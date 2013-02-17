import unittest
import tempfile
import shutil

import groundstation.node
import groundstation.transfer.response
from groundstation.station import Station


class MockStream(list):
    def enqueue(self, *args, **kwargs):
        self.append(*args, **kwargs)


def MockTERMINATE():
    pass


class MockStation(object):
    def __init__(self):
        self.tmpdir = tempfile.mkdtemp()
        self.node = groundstation.node.Node()
        self.station = Station(self.tmpdir, self.node)
        self.stream = MockStream()
        self.TERMINATE = MockTERMINATE

    def _Response(self, *args, **kwargs):
        kwargs['station'] = self.station
        return groundstation.transfer.response.Response(*args, **kwargs)

    def __del__(self):
        shutil.rmtree(self.tmpdir)

    @property
    def id(self):
        return "test_station"


class StationHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.station = MockStation()
