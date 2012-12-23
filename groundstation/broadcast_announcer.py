import socket
from broadcast_socket import BroadcastSocket

class BroadcastAnnouncer(BroadcastSocket):
    broadcast_payload = "PING"

    def __init__(self, port):
        super(BroadcastAnnouncer, self).__init__()
        self._addr = '255.255.255.255', port

    def ping(self):
        transmitted = self.socket.sendto(self.broadcast_payload, self._addr)
        if transmitted != len(self.broadcast_payload):
            # XXX Do we really care?
            pass
