import os
from support.station_fixture import StationTestCase, RandomPathTestCase

from groundstation.station import Station
from groundstation.gref import Gref, Tip


class TestStationObjectCache(StationTestCase):
    """Proves that querying for an unknown object returns false, then true"""
    def test_recently_queried(self):
        self.assertFalse(self.station.recently_queried("rawrtest"))
        self.assertTrue(self.station.recently_queried("rawrtest"))
        self.assertFalse(self.station.recently_queried("rawrtestSomeOther"))


class TestStationInit(RandomPathTestCase):
    def test_init(self):
        station = Station(self.path, None)
        self.assertEqual(station.store.path, self.path)


class TestSTationInitFromEnv(RandomPathTestCase):
    def test_init(self):
        old_gs_home = os.getenv('GROUNDSTATION_HOME')

        os.environ['GROUNDSTATION_HOME'] = self.path
        station = Station.from_env(None)
        self.assertEqual(station.store.path, self.path)
        if old_gs_home:
            os.environ['GROUNDSTATION_HOME'] = old_gs_home


class TestStationIterator(StationTestCase):
    def test_iterator(self):
        values = [1, 2, 3]
        return_values = [0, False]
        def iterator():
            while values:
                yield
                return_values[0] += values.pop()
            return_values[1] = True
            return
        self.station.register_iter(iterator)
        while self.station.has_ready_iterators():
            self.station.handle_iters()
        self.assertEqual(len(values), 0)
        self.assertEqual(return_values[0], 6)
        self.assertTrue(return_values[1])

    def test_ready_iterator(self):
        values = [1, 2]
        def iterator():
            while values:
                yield
                values.pop()
            return
        self.station.register_iter(iterator)
        # +1 is for the extra iteration to do cleanup
        for i in xrange(len(values) + 1):
            self.assertTrue(self.station.has_ready_iterators())
            self.station.handle_iters()
        self.assertFalse(self.station.has_ready_iterators())


class TestStationGrefs(StationTestCase):
    def test_channels(self):
        gref = Gref(self.station.store, "test_channel", "test_id")
        self.station.update_gref(gref, [Tip("foobar", "")], "")
        self.assertEqual(self.station.channels(), ["test_channel"])
