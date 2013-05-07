import os
import socket
import select

import unittest
import tempfile
import shutil

from collections import defaultdict

from groundstation.node import Node
from groundstation.station import Station

from groundstation.stream_listener import StreamListener
from groundstation.stream_client import StreamClient

from groundstation.peer_socket import PeerSocket

import groundstation.events.tcpnetwork_event as tcpnetwork_event


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
        current_station = [-1]

        def new_station():
            current_station[0] += 1
            return Station(os.path.join(self.dir, "station%d" % current_station[0]), self.node)

        self.stations = defaultdict(new_station)

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

        client.begin_handshake(self.stations[0])
        client.send()

        (sread, swrite, _) = tick()
        self.assertEqual(sread, [peer])

class StationHandshakeTestCase(StationIntegrationFixture):
    def test_handshake(self):
        active = self.stations["active"]
        passive = self.stations["passive"]

        read_sockets = [];
        write_sockets = [];
        def tick():
            tmp_write = []
            for sock in write_sockets:
                if sock.has_data_ready():
                    tmp_write.append(sock)
            sread, swrite, sexc = select.select(read_sockets, tmp_write, [], 1)
            if sexc:
                assert False, "Sockets kerploded"

            for i in swrite:
                if i.has_data_ready():
                    i.send()

            return sread

        addr = os.path.join(self.dir, "listener")
        listener = TestListener(addr)

        client = TestClient(addr)
        write_sockets.append(client)

        # Get our client
        peer = listener.accept(PeerSocket)
        read_sockets.append(peer)
        write_sockets.append(peer)

        # Start out handlshake
        client.begin_handshake(passive)
        client.send()
        sread = tick()

        self.assertEqual(len(sread), 1)
        self.assertIsInstance(sread[0], PeerSocket)
        for payload in tcpnetwork_event.payloads(sread[0]):
            gizmo = active.gizmo_factory.hydrate(payload, peer)
            self.assertEqual(gizmo.verb, "LISTDBHASH")
            self.assertEqual(gizmo.payload, "")
