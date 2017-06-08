from functools import wraps

from .exceptions import ClientError
from restapi.models import ChatRoom


def catch_client_error(func):
    @wraps(func)
    def inner(message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except ClientError as e:
            e.send_to(message.reply_channel)
    return inner


def get_room_or_error(room_id, user):

    try:
        room = ChatRoom.objects.get(pk=room_id)
    except ChatRoom.DoesNotExist:
        room_name = 'Room' + str(room_id)
        room = ChatRoom.objects.create(
            id=room_id,
            name=room_name
        )
        room.save()

    return room


def get_room_id_for_2_users(a, b):
    if a > b:
        a, b = b, a

    return ((a + b) * (a + b + 1)) / 2 + b + 1000
