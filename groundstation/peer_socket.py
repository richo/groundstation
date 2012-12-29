from sockets.socket_closed_exception import SocketClosedException
from sockets.stream_socket import StreamSocket


from groundstation import settings
import groundstation.logger
log = groundstation.logger.getLogger(__name__)

class PeerSocket(StreamSocket):
    """Wrapper for a peer who just connected, or one we've connected to

    Since the communication protocol should be implicitly bidirectional, the
    factory methods should be the only instanciation methods"""

    def __init__(self, conn, peer):
        self._sock = conn
        self.peer = peer
        self.write_queue = []
        #Intentioanlly don't call super(), we have a socket already

    @classmethod
    def from_accept(klass, args):
        return klass(*args)

    @classmethod
    def from_connect(klass, args):
        return klass(*args)

    def __repr__(self):
        return "<%s: from %s>" % (self.__class__, self.peer)

class PeerSocketClosedException(SocketClosedException):
    """Raised when a peer closes their socket"""
    pass
