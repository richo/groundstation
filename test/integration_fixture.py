import os
import socket
import tempfile
import unittest
import shutil

from groundstation.stream_listener import StreamListener
from groundstation.stream_client import StreamClient

from groundstation.node import Node
from groundstation.station import Station


class TestListener(StreamListener):
    def __init__(self, path):
        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        super(StreamListener, self).__init__()
        self._sock.bind(path)
        self._sock.listen(16)


class TestClient(StreamClient):
    def __init__(self, path):
        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        super(StreamClient, self).__init__()
        self.peer = path
        self.socket.connect(path)
        self.socket.setblocking(False)


class StationIntegrationFixture(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.node = Node()
        self.station = Station(os.path.join(self.dir, "station"), self.node)

    def tearDown(self):
        shutil.rmtree(self.dir)
