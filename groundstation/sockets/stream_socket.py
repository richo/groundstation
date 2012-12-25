import socket

import groundstation.logger
log = groundstation.logger.getLogger(__name__)

from groundstation.peer_socket import PeerSocket

class StreamSocket(object):
    """Wraps a TCP socket"""
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # XXX Implement the queue as a seperate class/
        self.write_queue  = []

    def fileno(self):
        """Return the underlying socket to make select() work"""
        return self._sock.fileno()

    @property
    def socket(self):
        return self._sock

    def accept(self):
        p = self._sock.accept()
        log.info("Accepted a connection from %s" % repr(p[1]))
        return PeerSocket.from_accept(p)

    def enqueue(self, data):
        """Enqueues data for writing inside the select loop"""
        self.write_queue.insert(0, data)

    def send(self):
        data = self.write_queue.pop()
        log.info("Attempting to write %i bytes" % (len(data)))
        self._sock.send(data)

    def has_data_ready(self):
        """(bool) does this socket have enqueued data ready"""
        return len(self.write_queue) > 0
