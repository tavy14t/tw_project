import time
import json
from channels import Channel
from channels.auth import channel_session_user_from_http, channel_session_user

from .settings import *
from .utils import get_room_or_error, catch_client_error
from .exceptions import ClientError
from restapi.models import *


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({'accept': True})
    message.channel_session['rooms'] = []


def ws_receive(message):
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)


@channel_session_user
def ws_disconnect(message):
    for room_id in message.channel_session.get("rooms", set()):
        try:
            room = ChatRoom.objects.get(pk=room_id)
            room.websocket_group.discard(message.reply_channel)
        except ChatRoom.DoesNotExist:
            pass


@channel_session_user
@catch_client_error
def chat_join(message):
    room = get_room_or_error(message["room"], message.user)
    user_query = Users.objects.get(userid=message['userid'])

    username = user_query.email

    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(
        set(message.channel_session['rooms']).union([room.id]))

    message.channel_session['userid'] = message['userid']
    message.channel_session['username'] = username
    message.channel_session['room'] = message["room"]

    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.channel_session['username'],
                          MSG_TYPE_ENTER)

    messages = Messages.objects.filter(
        to_roomid=message['room']).order_by('time')

    old_messages = []
    for obj in messages:
        username = Users.objects.get(userid=obj.from_userid).email
        old_messages.append({
            'username': username,
            'message': obj.message
        })

    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "title": message['name'],
            "last_messages": old_messages
        }),
    })


@channel_session_user
@catch_client_error
def chat_leave(message):
    room = get_room_or_error(message["room"], message.user)

    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.channel_session['username'],
                          MSG_TYPE_LEAVE)

    room.websocket_group.discard(message.reply_channel)
    message.channel_session['rooms'] = list(
        set(message.channel_session['rooms']).difference([room.id]))
    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(room.id),
        }),
    })


@channel_session_user
@catch_client_error
def chat_send(message):
    if int(message['room']) not in message.channel_session['rooms']:
        raise ClientError("ROOM_ACCESS_DENIED")

    username = message.channel_session['username']

    message_query = Messages.objects.create(
        from_userid=message.channel_session['userid'],
        to_roomid=message.channel_session['room'],
        message=message['message'],
        time=time.time()
    )
    message_query.save()

    room = get_room_or_error(message["room"], message.user)
    room.send_message(message["message"], username)
