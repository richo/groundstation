import groundstation.transfer.request

from groundstation.proto.git_object_pb2 import GitObject

from groundstation import logger
log = logger.getLogger(__name__)

def handle_fetchobject(self):
    log.info("Handling FETCHOBJECT")
    git_obj = self.station[self.payload]
    git_pb = GitObject()

    git_pb.type = git_obj.type
    git_pb.data = git_obj.read_raw()

    response = self._Response(self.id, "TRANSFER", git_pb.SerializeToString())
    self.stream.enqueue(response)
    self.TERMINATE()
