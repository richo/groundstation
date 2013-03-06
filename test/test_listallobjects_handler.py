from handler_fixture import StationHandlerTestCase

from groundstation.transfer.request_handlers import handle_listallobjects
from groundstation.transfer.response_handlers import handle_terminate
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

    def test_follows_up_on_channels(self):
        self.station.set_real_terminate(True)
        self.station.set_real_id(True)
        self.station.set_real_register(True)
        handle_listallobjects(self.station)
        req1 = self.station.stream.pop(0)
        self.assertEqual(req1.verb, "LISTALLOBJECTS")

        while self.station.stream:
            resp = self.station.stream.pop(0)
            if resp.verb == "TERMINATE":
                break
            self.assertEqual(resp.verb, "DESCRIBEOBJECTS")


        self.assertEqual(len(self.station.stream), 0)
        resp.stream = self.station.stream
        handle_terminate(req1)

        req2 = self.station.stream.pop(0)
        self.assertEqual(req2.verb, "LISTALLCHANNELS")


class TestHandlerListAllObjectsCached(StationHandlerTestCase):
    def test_has_cache(self):
        handle_listallobjects(self.station)
        req1 = self.station.stream.pop(0)
        self.assertEqual(req1.verb, "LISTALLOBJECTS")

        while self.station.stream:
            resp = self.station.stream.pop()
            self.assertEqual(resp.verb, "DESCRIBEOBJECTS")

        handle_listallobjects(self.station)
        resp = self.station.stream.pop(0)
        self.assertIsInstance(resp, response.Response)


class TestHandlerQueuesDeferredRetry(StationHandlerTestCase):
    def test_queues_retry(self):
        self.station.set_real_terminate(True)
        self.station.set_real_id(True)
        self.station.set_real_register(True)
        self.assertFalse(self.station.station.has_ready_deferreds())

        self.assertEqual(len(self.station.station.deferreds), 0)
        handle_listallobjects(self.station)
        req1 = self.station.stream.pop(0)
        handle_terminate(req1)
        self.assertEqual(len(self.station.station.deferreds), 1)
