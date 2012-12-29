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
        self._sock.connect((addr, settings.PORT))

    def begin_handshake(self):
        request = Request("LISTALLOBJECTS")
        self.enqueue(request)


    def recv(self):
        """Recieve some bytes fromt he socket, handling buffering internally"""
        # TODO Duped with PeerSocket
        data = self.socket.recv(settings.DEFAULT_BUFSIZE)
        if not data:
            self.socket.close()
            raise StreamSocketClosedException(self)
        log.debug("RECV %i bytes: %s from %s" %
                (len(data), repr(data), self.peer))
        return data # TODO Buffering

class StreamSocketClosedException(SocketClosedException):
    """Raised when a peer closes their socket"""
    pass
