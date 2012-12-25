import socket
from sockets.broadcast_socket import BroadcastSocket

import logger
log = logger.getLogger(__name__)

class BroadcastDiscoverer(BroadcastSocket):

    def __init__(self, port):
        super(BroadcastDiscoverer, self).__init__()
        self.socket.bind(('0.0.0.0', port))

    def __del__(self):
        "Shutdown and close the underlying socket."
        self._sock.close()

    @property
    def timeout(self):
        'Receive timeout'
        return self._sock.gettimeout()

    @timeout.setter
    def timeout(self, value):
        self._sock.settimeout(value)

    def recv(self, size):
        "Receive a broadcast through the underlying socket."
        return self._sock.recvfrom(size)

