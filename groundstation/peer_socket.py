import groundstation.logger
log = groundstation.logger.getLogger(__name__)

class PeerSocket(object):
    """Wrapper for a peer who just connected, or one we've connected to

    Since the communication protocol should be implicitly bidirectional, the
    factory methods should be the only instanciation methods"""

    def __init__(self, conn, peer):
        self.conn = conn
        self.peer = peer
        self.queue = []

    @classmethod
    def from_accept(klass, args):
        return klass(*args)

    @classmethod
    def from_connect(klass, args):
        return klass(*args)

    def fileno(self):
        return self.conn.fileno()

    def __repr__(self):
        return "<%s: from %s>" % (self.__class__, self.peer)

    def has_data_ready(self):
        return len(self.queue) > 0

    def enqueue(self, data):
        self.queue.insert(0, data)

    def recv(self):
        """Recieve some bytes fromt he socket, handling buffering internally"""
        data = self.conn.recv(1024)
        log.debug("RECV %i bytes: %s from %s" %
                (len(data), repr(data), self.peer))
        return data # TODO Buffering

    def send(self):
        """Send some data that's presently in the queue"""
        assert self.has_data_ready(), "Attempt to send without data ready"
        data = self.queue.pop()
        log.debug("SEND %i bytes: %s to %s" %
                (len(data), repr(data), self.peer))
        self.conn.send(data)
