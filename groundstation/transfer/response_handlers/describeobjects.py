import groundstation.proto.object_list_pb2

from groundstation import logger
log = logger.getLogger(__name__)


def handle_describeobjects(self):
    if not self.payload:
        log.info("station %s sent empty DESCRIBEOBJECTS payload - new database?" % (str(self.origin)))
        return
    objects = groundstation.proto.object_list_pb2.ObjectList()
    objects.ParseFromString(self.payload)
    for obj in objects.objectname:
        if obj not in self.station:
            request = self._Request("FETCHOBJECT", payload=obj)
            self.stream.enqueue(request)
        else:
            log.debug("Not fetching already present object %s" % (str(obj)))
