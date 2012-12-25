import socket

class BroadcastSocket(object):
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    def fileno(self):
        """Return the underlying socket to make select() work"""
        return self._sock.fileno()

    @property
    def socket(self):
        return self._sock



