import pygit2
from groundstation.utils import oid2hex
from support.handler_fixture import StationHandlerTestCase, MockRequest

from groundstation.proto.git_object_pb2 import GitObject

from groundstation.transfer.response_handlers import handle_transfer
from groundstation.transfer.response_handlers.transfer import UnsolicitedTransfer


class TestHandlerTransfer(StationHandlerTestCase):
    def test_transfer_object(self):
        self.station.set_real_id(True)

        object_body = "foo bar baz butts lol"
        oid = pygit2.hash(object_body)

        req = MockRequest(self.station.id)
        req.payload = oid2hex(oid)

        self.station.station.registry.register(req)

        git_pb = GitObject()
        git_pb.data = object_body
        git_pb.type = pygit2.GIT_OBJ_BLOB
        self.station.payload = git_pb.SerializeToString()
        handle_transfer(self.station)

        self.assertTrue(self.station.station[oid2hex(oid)], object_body)

    def test_rejects_invalid_transfers(self):
        self.station.set_real_id(True)

        object_body = "foo bar baz butts lol"

        req = MockRequest(self.station.id)
        req.payload = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"

        self.station.station.registry.register(req)

        git_pb = GitObject()
        git_pb.data = object_body
        git_pb.type = pygit2.GIT_OBJ_BLOB
        self.station.payload = git_pb.SerializeToString()
        self.assertRaises(AssertionError, handle_transfer, self.station)

    def test_rejects_unsolicited_transfers(self):
        self.station.set_real_id(True)

        object_body = "foo bar baz butts lol"

        git_pb = GitObject()
        git_pb.data = object_body
        git_pb.type = pygit2.GIT_OBJ_BLOB
        self.station.payload = git_pb.SerializeToString()
        self.assertRaises(UnsolicitedTransfer, handle_transfer, self.station)
