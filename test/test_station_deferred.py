import time

from support.station_fixture import StationTestCase

from groundstation.deferred import Deferred, defer_until


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

        for i in xrange(10):
            import sys
            # sys.stderr.write("Registering deferred %i" % i)
            @self.station.register_deferred
            @defer_until(now - 30)
            def thunk():
                ret[0] += 1

        self.assertEqual(len(self.station.deferreds), 10)

        self.station.handle_deferreds()

        self.assertEqual(len(self.station.deferreds), 0)
        self.assertEqual(ret[0], 10)
