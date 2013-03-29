from handler_fixture import StationHandlerTestCase

from groundstation.transfer.notification_handlers import handle_newobject


class TestHandlerNewObject(StationHandlerTestCase):
    def test_fetches_nonexistant_objects(self):
        oid = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
        self.station.payload = oid
        handle_newobject(self.station)

        req = self.station.stream.pop(0)
        self.assertEqual(req.verb, "FETCHOBJECT")
        self.assertEqual(req.payload, oid)

    def test_does_not_fetch_existing_objects(self):
        oid = self.station.station.write("ButtsLol")
        self.station.payload = oid
        handle_newobject(self.station)

        self.assertEqual(0, len(self.station.stream))
