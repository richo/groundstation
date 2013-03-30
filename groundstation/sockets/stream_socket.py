import socket
import errno
from groundstation import settings
from groundstation.transfer.response import Response
from socket_closed_exception import SocketClosedException

import groundstation.logger
log = groundstation.logger.getLogger(__name__)

class StreamSocket(object):
    """Base class for conversational protocols

    If you don't want a socket allocated (ie, you already have one) set it to
    ._sock before calling __init__"""
    def __init__(self):
        if not hasattr(self, "_sock"):
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # XXX Implement the queue as a seperate class/
        self.write_queue = []
        self.packet_queue = []
        self.buffer = ""

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

    def _dequeue(self):
        payload = self.write_queue.pop()
        if isinstance(payload, str):
            data = self.serialize(payload)
            return "%i%s%s" % (len(data), chr(0), data)
        elif isinstance(payload, tuple):
            return payload[0]
        else:
            raise Exception("Invalid type: %s" % (type(payload)))

    def send(self):
        """Send some data that's presently in the queue"""
        assert self.has_data_ready(), "Attempt to send without data ready"
        data = self._dequeue()
        len_data = len(data)

        log.debug("SEND %i bytes to %s" %
                # XXX Ignore warnings, subclasses implement self.peer
                (len_data, self.peer))
        # Send the number of bytes to read in ascii, and then a nul
        # TODO Buffer this out to amke sure that we don't block.
        idx = 0
        while idx < len_data:
            try:
                idx += self.socket.send(data[idx:])
            except socket.error as e:
                if e.errno == errno.EWOULDBLOCK:
                    # Put the remaining bytes back on the stack for the next
                    # run through the event loop
                    self.write_queue.append((data[idx:],))
                    return False
                elif e.errno == errno.EBADF:
                    # Connection has been closed. Nuke it.
                    self.close_and_finalise()
                else:
                    raise
        return True


    def has_data_ready(self):
        """(bool) does this socket have enqueued data ready"""
        return len(self.write_queue) > 0

    def recv(self):
        """Recieve some bytes fromt he socket, handling buffering internally"""
        # TODO Build a queue that we can pop objects out o
        self.recv_to_buffer()
        assert chr(0) in self.buffer, \
                'NUL not in buffer, something has gone awfully wrong'

        tmp_buffer = self.buffer
        iterations = 0
        while True:
            if not tmp_buffer: # Catch having emptied our buffer
                break
            # Keep the unmolested buffer
            segment_length, _, payload_buffer = tmp_buffer.partition(chr(0))
            segment_length = int(segment_length)
            if len(payload_buffer) >= segment_length:
                iterations += 1
                # We have the whole buffer
                data = payload_buffer[:segment_length]
                payload_buffer = payload_buffer[segment_length:]
                log.debug("RECV %i bytes from %s" %
                        # XXX Ignore, subclasses set .peer
                        (len(data), self.peer))
                self.packet_queue.insert(0, data)
                tmp_buffer = payload_buffer
                # Bail if we emptied the buffer
            else:
                # We haven't touched tmp_buffer, it is therefore safe to save
                # back to the classbuffer
                if iterations == 0:
                    log.warn("Didn't construct a single full payload!")
                break
        self.buffer = tmp_buffer

    @staticmethod
    def serialize(payload):
        if isinstance(payload, Response):
            return payload.SerializeToString()
        else:
            return payload

    def recv_to_buffer(self):
        try:
            data = self.socket.recv(settings.DEFAULT_BUFSIZE)
        except socket.error as e:
            if e.errno == errno.ECONNRESET:
                data = None
            else:
                raise e
        if not data:
            self.socket.close()
            self.close_and_finalise()
        self.buffer = self.buffer + data

    def close_and_finalise(self):
        raise SocketClosedException(self, self.peer)
