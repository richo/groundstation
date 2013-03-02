import pygit2
from groundstation.utils import oid2hex
from handler_fixture import StationHandlerTestCase
import git_fixture

from groundstation.proto.git_object_pb2 import GitObject

from groundstation.transfer.response_handlers import handle_transfer


def git_object(body, type):
        git_pb = GitObject()
        git_pb.data = body
        git_pb.type = type
        return git_pb


class TestHandlerTransfer(StationHandlerTestCase):
    def test_transfer_object(self):
        object_body = "foo bar baz butts lol"
        oid = pygit2.hash(object_body)
        git_pb = git_object(object_body, pygit2.GIT_OBJ_BLOB)
        self.station.payload = git_pb.SerializeToString()
        handle_transfer(self.station)

        self.assertTrue(self.station.station[oid2hex(oid)], object_body)

    def test_transfer_tree(self):
        tree_body = git_fixture.fake_tree()
        oid = pygit2.hash(tree_body)
        git_pb = git_object(tree_body, pygit2.GIT_OBJ_TREE)
        self.station.payload = git_pb.SerializeToString()
        handle_transfer(self.station)

        obj = self.station.station[oid2hex(oid)]
        self.assertTrue(obj, tree_body)
