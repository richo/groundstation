import socket

class StreamListener(object):
    """Wraps a TCP socket"""
    def __init__(self, port):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind(('0.0.0.0', port))
        self._sock.listen(16)

    def fileno(self):
        """Return the underlying socket to make select() work"""
        return self._sock.fileno()

    @property
    def socket(self):
        return self._sock

    def accept(self):
        return self._sock.accept()
