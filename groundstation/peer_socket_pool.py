import logger
log = logger.getLogger(__name__)

class PeerSocketPool(list):
    """
    Encapsulates a pool of PeerSockets.

    Correctly replies to PeerSocket in Pool
    """

    def __contains__(self, other):
        for i in self:
            if i.peer == other:
                return True
        return False
