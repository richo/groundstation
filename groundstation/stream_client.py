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
        request = Request("LISTDBHASH", payload="", station=station, stream=self)
        station.register_request(request)
        self.enqueue(request)

    def begin_incremental_sync(self, station):
        prefixes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    'a', 'b', 'c', 'd', 'e', 'f']

        def terminate(self):
            if not prefixes:
                pass
            prefix = prefixes.pop(0)
            request = Request("LISTDBHASH", payload=prefix, station=station, stream=self)
            request.terminate = terminate
            station.register_request(request)
            self.enqueue(request)

        # Our terminate handler kicks of a fetch of the next DB hash prefix. We
        # bump it to start the handshake.
        terminate(self)
