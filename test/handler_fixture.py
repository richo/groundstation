import unittest
import tempfile
import shutil
import uuid

import groundstation.node
import groundstation.transfer.response
import groundstation.transfer.request
from groundstation.station import Station


class MockStream(list):
    def enqueue(self, *args, **kwargs):
        self.append(*args, **kwargs)


def MockTERMINATE():
    pass


class MockStation(object):
    def __init__(self, **kwargs):
        self.tmpdir = tempfile.mkdtemp()
        self.node = groundstation.node.Node()
        self.station = Station(self.tmpdir, self.node)
        self.stream = MockStream()
        self.TERMINATE = MockTERMINATE
        self.id = "test_station"

        if 'origin' in kwargs:
            self.origin = kwargs['origin']
        else:
            self.origin = uuid.uuid1()

    def _Response(self, *args, **kwargs):
        kwargs['station'] = self.station
        return groundstation.transfer.response.Response(*args, **kwargs)

    def _Request(self, *args, **kwargs):
        kwargs['station'] = self.station
        return groundstation.transfer.request.Request(*args, **kwargs)

    def __del__(self):
        shutil.rmtree(self.tmpdir)

    def teardown(self):
        pass

    def set_real_id(self, value):
        self.id = uuid.uuid1()

    def set_real_terminate(self, value):
        if value:
            self.TERMINATE = lambda: groundstation.transfer.request.TERMINATE(self)
        else:
            self.TERMINATE = MockTERMINATE

    def set_real_register(self, value):
        self.station.station.registry.register(self.station)

class StationHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.station = MockStation()
