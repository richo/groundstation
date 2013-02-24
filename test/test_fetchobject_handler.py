import pygit2

from handler_fixture import StationHandlerTestCase

from groundstation.transfer.request_handlers import handle_fetchobject
from groundstation.proto.object_list_pb2 import ObjectList
from groundstation.proto.git_object_pb2 import GitObject


class TestHandlerFetchObject(StationHandlerTestCase):
    def test_handle_fetchobject(self):
        obj = self.station.station.write("foobarbazlulz")
        self.station.payload = obj
        handle_fetchobject(self.station)
        response = self.station.stream.pop()
        pb_obj = GitObject()
        pb_obj.ParseFromString(response.payload)
        self.assertEqual(pb_obj.type, pygit2.GIT_OBJ_BLOB)
        self.assertEqual(pb_obj.data, "foobarbazlulz")

    def handle_fetch_nonexistant_object(self):
        pass
