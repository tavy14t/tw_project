from channels import include


from channels import route
from .consumers import *

websocket_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_receive),
    route("websocket.disconnect", ws_disconnect),
]

custom_routing = [
    route("chat.receive", chat_join, command="^join$"),
    route("chat.receive", chat_leave, command="^leave$"),
    route("chat.receive", chat_send, command="^send$"),
]

channel_routing = [
    include("trex.routing.websocket_routing", path=r"^/chat/stream"),
    include("trex.routing.custom_routing"),
]
