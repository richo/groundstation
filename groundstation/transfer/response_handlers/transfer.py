import pygit2
from groundstation.proto.git_object_pb2 import GitObject

from groundstation import logger
log = logger.getLogger(__name__)


def handle_transfer(self):
    git_pb = GitObject()
    git_pb.ParseFromString(self.payload)
    log.info("Handling TRANSFER of %s" % (git_pb.type))
    if git_pb.type == pygit2.GIT_OBJ_BLOB:
        req = self.station.get_request(self.id)
        assert req.payload == pygit2.hash(git_pb.data), \
            "Attempted to be sent invalid object for %s" % (req.payload)
    ret = self.station.store.write(git_pb.type, git_pb.data)
    log.info("Wrote object %s into local db" % logger.fix_oid(ret))
