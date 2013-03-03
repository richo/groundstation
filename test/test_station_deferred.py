import time

from station_fixture import StationTestCase

from groundstation.deferred import Deferred


class TestStationDeferreds(StationTestCase):
    def test_ready_deferred(self):
        now = time.time()
        deferred = Deferred(now - 10, None)
        self.station.register_deferred(deferred)
        self.assertEqual(len(self.station.deferreds), 1)
        self.assertTrue(self.station.has_ready_deferreds())

    def test_unready_deferred(self):
        now = time.time()
        deferred = Deferred(now + 60, None)
        self.station.register_deferred(deferred)
        self.assertEqual(len(self.station.deferreds), 1)
        self.assertFalse(self.station.has_ready_deferreds())

    def test_handle_deferred(self):
        now = time.time()
        ret = [0]

        def thunk():
            ret[0] += 1

        deferred = Deferred(now - 10, thunk)
        self.station.register_deferred(deferred)
        self.station.register_deferred(deferred)
        self.station.register_deferred(deferred)
        self.station.handle_deferreds()
        self.assertEqual(ret[0], 3)
