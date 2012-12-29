from station_fixture import StationTestCase

class TestStationObjectCache(StationTestCase):
    """Proves that querying for an unknown object returns false, then true"""
    def test_recently_queried(self):
        self.assertFalse(self.station.recently_queried("rawrtest"))
        self.assertTrue(self.station.recently_queried("rawrtest"))
        self.assertFalse(self.station.recently_queried("rawrtestSomeOther"))

