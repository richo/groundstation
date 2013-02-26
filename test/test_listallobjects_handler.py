from handler_fixture import StationHandlerTestCase

from groundstation.transfer.request_handlers import handle_listallobjects
import groundstation.transfer.response as response

from groundstation.proto.object_list_pb2 import ObjectList


class TestHandlerListAllObjects(StationHandlerTestCase):
    def test_handle_listallobjects_returns_stream_for_few_objects(self):
        # Make ourselves cached
        self.station.station.mark_queried(self.station.origin)
        oids = list()
        for i in xrange(64):
            oids.append(self.station.station.write("test_%i" % (i)))

        handle_listallobjects(self.station)
        resp = self.station.stream.pop()
        self.assertIsInstance(resp, response.Response)
        objects = ObjectList()
        objects.ParseFromString(resp.payload)

        self.assertEqual(len(objects.objectname), len(oids))

        for i in objects.objectname:
            self.assertIn(i, oids)


class TestHandlerListAllObjectsCached(StationHandlerTestCase):
    def test_has_cache(self):
        handle_listallobjects(self.station)
        req1 = self.station.stream.pop(0)
        self.assertEqual(req1.verb, "LISTALLOBJECTS")
        req2 = self.station.stream.pop(0)
        self.assertEqual(req2.verb, "LISTALLCHANNELS")

        while self.station.stream:
            self.station.stream.pop()

        handle_listallobjects(self.station)
        resp = self.station.stream.pop(0)
        self.assertIsInstance(resp, response.Response)
