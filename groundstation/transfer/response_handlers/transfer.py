import pygit2
from groundstation.proto.git_object_pb2 import GitObject
import groundstation.utils as utils

from groundstation import logger
log = logger.getLogger(__name__)


class UnsolicitedTransfer(Exception):
    pass


def handle_transfer(self):
    git_pb = GitObject()
    git_pb.ParseFromString(self.payload)
    log.info("Handling TRANSFER of %s" % (git_pb.type))

    try:
        req = self.station.get_request(self.id)
    except KeyError:
        raise UnsolicitedTransfer

    if git_pb.type == pygit2.GIT_OBJ_BLOB:
        data_hash = utils.oid2hex(pygit2.hash(git_pb.data))
        assert req.payload == data_hash, \
            "Attempted to be sent invalid object for %s; got %s" % (req.payload, data_hash)
    ret = self.station.store.write(git_pb.type, git_pb.data)
    log.info("Wrote object %s into local db" % logger.fix_oid(ret))
