import socket
from sockets.stream_socket import StreamSocket
from sockets.socket_closed_exception import SocketClosedException
from transfer.request import Request
import settings

import groundstation.logger
log = groundstation.logger.getLogger(__name__)

class StreamClient(StreamSocket):
    def __init__(self, addr):
        self.peer = addr
        super(StreamClient, self).__init__()
        self.socket.connect((addr, settings.PORT))

    def begin_handshake(self):
        request = Request("LISTALLOBJECTS")
        self.enqueue(request)
