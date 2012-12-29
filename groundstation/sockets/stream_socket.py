import socket
from groundstation import settings
from groundstation.transfer.response import Response
from socket_closed_exception import SocketClosedException

import groundstation.logger
log = groundstation.logger.getLogger(__name__)

class StreamSocket(object):
    """Wraps a TCP socket"""
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # XXX Implement the queue as a seperate class/
        self.write_queue  = []

    def fileno(self):
        return self.socket.fileno()

    @property
    def socket(self):
        return self._sock

    def accept(self, klass):
        p = self._sock.accept()
        log.info("Accepted a connection from %s" % repr(p[1]))
        # Return more instances of ourself.
        return klass.from_accept(p)

    def enqueue(self, data):
        """Enqueues data for writing inside the select loop"""
        if hasattr(data, "SerializeToString"):
            data = data.SerializeToString()
        self.write_queue.insert(0, data)

    def send(self):
        """Send some data that's presently in the queue"""
        assert self.has_data_ready(), "Attempt to send without data ready"
        data = self.serialize(self.write_queue.pop())
        log.debug("SEND %i bytes: %s to %s" %
                # XXX Ignore warnings, subclasses implement self.peer
                (len(data), repr(data), self.peer))
        # Send the number of bytes to read in ascii, and then a nul
        # TODO Buffer this out to amke sure that we don't block.
        self.socket.send("%i%s" % (len(data), chr(0)))
        self.socket.send(data)


    def has_data_ready(self):
        """(bool) does this socket have enqueued data ready"""
        return len(self.write_queue) > 0

    def recv(self):
        """Recieve some bytes fromt he socket, handling buffering internally"""
        # TODO Duped with PeerSocket
        data = self.socket.recv(settings.DEFAULT_BUFSIZE)
        if not data:
            self.socket.close()
            raise SocketClosedException(self)
        log.debug("RECV %i bytes: %s from %s" %
                (len(data), repr(data), self.peer))
        return data # TODO Buffering

    @staticmethod
    def serialize(payload):
        if isinstance(payload, Response):
            return payload.SerializeToString()
        else:
            return payload

