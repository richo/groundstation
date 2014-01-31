import socket
import logger
from sockets.broadcast_socket import BroadcastSocket, BroadcastUnrouteable

import logger
log = logger.getLogger(__name__)


class BroadcastAnnouncer(BroadcastSocket):
    def __init__(self, port, address = None):
        super(BroadcastAnnouncer, self).__init__()
        broadcast_address = address or '255.255.255.255'
        self._addr = broadcast_address, port
        self._name = None
        self.broadcast_payload = "PING None"

    @property
    def name(self):
        return self._name

    # TODO: Make this accept a Node to build the payload from

    @name.setter
    def name(self, value):
        self._name = value
        self.broadcast_payload = "PING %s" % (self._name)

    def ping(self):
        log.info("ping payload: %s" % (self.broadcast_payload))
        try:
            transmitted = self.socket.sendto(self.broadcast_payload, self._addr)
        except socket.error as e:
            if e.errno == 65:  # No route to host
                raise BroadcastUnrouteable(e)
            else:
                raise e
        if transmitted != len(self.broadcast_payload):
            log.warning("ping wasn't successfully broadcast")
