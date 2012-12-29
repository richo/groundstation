import socket
from sockets.stream_socket import StreamSocket
from sockets.socket_closed_exception import SocketClosedException
import settings

class StreamClient(StreamSocket):
    def __init__(self, addr):
        self.peer = addr
        super(StreamClient, self).__init__()
        self._sock.connect((addr, settings.PORT))

    def begin_handshake(self):
        self.enqueue("LISTALLOBJECTS")

    def recv(self):
        return self.socket.recv(settings.DEFAULT_BUFSIZE)

class StreamSocketClosedException(SocketClosedException):
    """Raised when a peer closes their socket"""
    pass
