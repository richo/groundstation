import logger
log = logger.getLogger(__name__)

class PeerSocketPool(list):
    """
    Encapsulates a pool of PeerSockets.

    Correctly replies to PeerSocket in Pool
    """
    def __init__(self, *args, **kwargs):
        super(list, self).__init__(self, *args, **kwargs)
        self.purged_connections = []

    def purge(self, peer):
        self.purged_connections.remove(peer)

    def remove(self, other):
        if other.peer in self.purged_connections:
            return False
        for idx, i in enumerate(self):
            if i.peer == other.peer:
                conn = self.pop(idx)
                self.purged_connections.append(conn.peer)
                return conn
        raise AttributeError("%s has no attribute %s" %
                    (type(self), repr(other)))

    def __contains__(self, other):
        for i in self:
            if i.peer == other:
                return True
        return False

    def __getitem__(self, key):
        for i in self:
            if i.peer == key:
                return i
        raise KeyError
