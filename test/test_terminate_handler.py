from support.handler_fixture import StationHandlerTestCase

from groundstation.transfer.request_handlers import handle_fetchobject
from groundstation.transfer.response_handlers import handle_terminate


class TestHandlerTerminate(StationHandlerTestCase):
    def test_handle_terminate(self):
        # Write an object into the station
        self.station.set_real_id(True)
        oid = self.station.station.write("butts lol")
        self.station.payload = oid

        self.assertEqual(len(self.station.station.registry.contents), 0)

        self.station.station.register_request(self.station)
        self.assertEqual(len(self.station.station.registry.contents), 1)

        handle_fetchobject(self.station)
        ret = [0]

        def _teardown():
            ret[0] += 1
        self.station.teardown = _teardown

        term = self.station.stream.pop()
        handle_terminate(term)

        self.assertEqual(len(self.station.station.registry.contents), 0)
        self.assertEqual(ret[0], 1)
