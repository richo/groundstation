from sockets.stream_socket import StreamSocket
import socket

from groundstation import settings
import groundstation.logger
log = groundstation.logger.getLogger(__name__)

class PeerSocket(StreamSocket):
    """Wrapper for a peer who just connected, or one we've connected to

    Since the communication protocol should be implicitly bidirectional, the
    factory methods should be the only instanciation methods"""

    def __init__(self, conn, peer):
        self._sock = conn
        super(PeerSocket, self).__init__()
        self.peer = peer

    @classmethod
    def from_accept(klass, args):
        return klass(*args)

    @classmethod
    def from_connect(klass, args):
        return klass(*args)

    def __repr__(self):
        return "<%s: from %s>" % (self.__class__, self.peer)

    # Wrap StreamSocket's send and recv in exception handling
    def send(self, *args, **kwargs):
        try:
            return super(PeerSocket, self).send(*args, **kwargs)
        except socket.error as e:
            self.close_and_finalise()

    def recv(self, *args, **kwargs):
        try:
            return super(PeerSocket, self).recv(*args, **kwargs)
        except socket.error as e:
            self.close_and_finalise()
