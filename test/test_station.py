from station_fixture import StationTestCase

class TestStationObjectCache(StationTestCase):
    """Proves that querying for an unknown object returns false, then true"""
    def test_recently_queried(self):
        self.assertFalse(self.station.recently_queried("rawrtest"))
        self.assertTrue(self.station.recently_queried("rawrtest"))
        self.assertFalse(self.station.recently_queried("rawrtestSomeOther"))

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
