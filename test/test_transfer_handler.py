import pygit2
from groundstation.utils import oid2hex
from handler_fixture import StationHandlerTestCase

from groundstation.proto.git_object_pb2 import GitObject

from groundstation.transfer.response_handlers import handle_transfer


class TestHandlerTransfer(StationHandlerTestCase):
    def test_transfer_object(self):
        object_body = "foo bar baz butts lol"
        oid = pygit2.hash(object_body)
        git_pb = GitObject()
        git_pb.data = object_body
        git_pb.type = pygit2.GIT_OBJ_BLOB
        self.station.payload = git_pb.SerializeToString()
        handle_transfer(self.station)

        self.assertTrue(self.station.station[oid2hex(oid)], object_body)
