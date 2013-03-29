import groundstation.proto.object_list_pb2

from groundstation import logger
log = logger.getLogger(__name__)


def handle_newobject(self):
    obj = self.payload
    if obj not in self.station:
        request = self._Request("FETCHOBJECT", payload=obj)
        self.stream.enqueue(request)
