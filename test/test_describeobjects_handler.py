import random
from handler_fixture import StationHandlerTestCase

from groundstation.proto.object_list_pb2 import ObjectList
from groundstation.proto.object_list_pb2 import ObjectList

from groundstation.transfer.response_handlers import handle_describeobjects


def _payload(ids):
    chunk = ObjectList()
    for i in ids:
        chunk.objectname.append(i)
    return chunk.SerializeToString()


class TestHandlerDescribeObjects(StationHandlerTestCase):
    def test_handle_describeobjects(self):
        real_objects = []
        for i in xrange(20):
            real_objects.append(self.station.station.write("lulz%i" % (i)))

        fake_objects = [
                'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
                'cccccccccccccccccccccccccccccccccccccccc',
                'dddddddddddddddddddddddddddddddddddddddd',
                'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
                ]

        self.station.payload = _payload(real_objects + fake_objects)

        handle_describeobjects(self.station)

        requested_ids = []

        for i in self.station.stream:
            requested_ids.append(i.payload)

        for i in real_objects:
            self.assertNotIn(i, requested_ids)

        for i in fake_objects:
            self.assertIn(i, requested_ids)
