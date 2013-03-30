import socket
from sockets.stream_socket import StreamSocket

class StreamListener(StreamSocket):
    def __init__(self, port):
        super(StreamListener, self).__init__()
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(('0.0.0.0', port))
        self._sock.listen(16)
