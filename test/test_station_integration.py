import os
import socket
import select

import unittest
import tempfile
import shutil

from groundstation.peer_socket import PeerSocket

from integration_fixture import StationIntegrationFixture, \
                                TestListener, \
                                TestClient



class StationConnectionTestCase(StationIntegrationFixture):
    def test_two_stations_connect(self):
        addr = os.path.join(self.dir, "listener")
        listener = TestListener(addr)
        client = TestClient(addr)


class StationCommunication(StationIntegrationFixture):
    def test_send_objects(self):
        read_sockets = []
        write_sockets = []
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
