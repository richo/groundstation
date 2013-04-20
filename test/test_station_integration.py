import os
import socket
import select

import unittest
import tempfile
import shutil

from groundstation.node import Node
from groundstation.station import Station

from groundstation.stream_listener import StreamListener
from groundstation.stream_client import StreamClient

from groundstation.peer_socket import PeerSocket


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


class StationConnectionTestCase(StationIntegrationFixture):
    def test_two_stations_connect(self):
        addr = os.path.join(self.dir, "listener")
        listener = TestListener(addr)
        client = TestClient(addr)


class StationCommunication(StationIntegrationFixture):
    def test_send_objects(self):
        read_sockets = [];
        write_sockets = [];
        def tick():
            return select.select(read_sockets, write_sockets, [], 1)

        addr = os.path.join(self.dir, "listener")
        listener = TestListener(addr)
        read_sockets.append(listener)

        client = TestClient(addr)
        write_sockets.append(client)

        (sread, swrite, _) = tick()
        # Handle our listener
        self.assertEqual(len(sread), 1)
        peer = listener.accept(PeerSocket)
        read_sockets.append(peer)
        write_sockets.append(peer)

        self.assertEqual(len(swrite), 1)

        client.begin_handshake(self.station)
        client.send()

        (sread, swrite, _) = tick()
        self.assertEqual(sread, [peer])
