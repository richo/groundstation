import os
import socket

import unittest
import tempfile

from groundstation.stream_listener import StreamListener
from groundstation.stream_client import StreamClient


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

class StationConnectionTestCase(StationIntegrationFixture):
    def test_two_stations_connect(self):
        addr = os.path.join(self.dir, "listener")
        listener = TestListener(addr)
        client = TestClient(addr)
