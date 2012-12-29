import groundstation.logger
log = groundstation.logger.getLogger(__name__)

class SocketClosedException(Exception):
    """Raised when a peer closes their socket"""
    def __init__(self, peer):
        log.info("Peer %s closed connection" % (str(peer.peer)))
        self.peer = peer
