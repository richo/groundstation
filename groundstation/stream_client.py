from sockets.stream_socket import StreamSocket
from transfer.request import Request
import settings

import groundstation.logger
log = groundstation.logger.getLogger(__name__)


class StreamClient(StreamSocket):
    def __init__(self, addr):
        super(StreamClient, self).__init__()
        # TODO Pretty sure this should be a struct sockaddr
        self.peer = addr
        self.socket.connect((addr, settings.PORT))
        self.socket.setblocking(False)

    def begin_handshake(self, station):
        request = Request("LISTALLOBJECTS", station=station, stream=self)
        station.register_request(request)
        self.enqueue(request)
