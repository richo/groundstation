import tempfile
import shutil
import unittest

from groundstation.node import Node
from groundstation.station import Station


class StationTestCase(unittest.TestCase):
    def setUp(self):
        self.node = Node()
        self.station = Station(tempfile.mkdtemp(), self.node)

    def tearDown(self):
        shutil.rmtree(self.station.store.path)
