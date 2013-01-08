from groundstation.proto.git_object_pb2 import GitObject

from groundstation import logger
log = logger.getLogger(__name__)


def handle_transfer(self):
    git_pb = GitObject()
    git_pb.ParseFromString(self.payload)
    log.info("Handling TRANSFER of %s" % (git_pb.type))
    ret = self.station.repo.write(git_pb.type, git_pb.data)
    log.info("Wrote object %s" % (repr(ret)))
