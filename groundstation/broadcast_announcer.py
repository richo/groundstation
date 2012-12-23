import socket
from broadcast_socket import BroadcastSocket

class BroadcastAnnouncer(BroadcastSocket):
    def __init__(self, port):
        super(BroadcastAnnouncer, self).__init__()
        self._addr = '255.255.255.255', port
        self._name = None
        self.broadcast_payload = "PING None"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.broadcast_payload = "PING %s" % (self._name)

    def ping(self):
        transmitted = self.socket.sendto(self.broadcast_payload, self._addr)
        if transmitted != len(self.broadcast_payload):
            # XXX Do we really care?
            pass
