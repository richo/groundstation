from sockets.stream_socket import StreamSocket
from transfer.notification import Notification
import settings

from groundstation.utils import path2id

import groundstation.logger
log = groundstation.logger.getLogger(__name__)


class StreamClient(StreamSocket):
    def __init__(self, addr):
        super(StreamClient, self).__init__()
        # TODO Pretty sure this should be a struct sockaddr
        self.peer = addr
        self.socket.connect((addr, settings.PORT))
        self.socket.setblocking(False)

    def notify_new_object(self, station, path):
        # TODO FSWatcher should probably be responsible for catching these to
        # keep signal:noise sane
        obj = path2id(path)
        notification = Notification("NEWOBJECT", station=station, stream=self, payload=obj)
        self.enqueue(notification)
