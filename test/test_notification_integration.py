import os
import select

import groundstation.fs_watcher as fs_watcher
from groundstation.peer_socket import PeerSocket

from groundstation.utils import path2id

from integration_fixture import StationIntegrationFixture, \
                                TestListener, \
                                TestClient

class StationFSWatcherIntegration(StationIntegrationFixture):
    def test_notifies_peer(self):
        read_sockets = []
        write_sockets = []
        def tick():
            return select.select(read_sockets, write_sockets, [], 1)

        addr = os.path.join(self.dir, "listener")
        listener = TestListener(addr)
        client = TestClient(addr)
        peer = listener.accept(PeerSocket)
        watcher = fs_watcher.FSWatcher(self.stations[0].store.object_root)

        read_sockets.append(client)
        read_sockets.append(watcher)
        self.stations[0].write("trolololol")
        (sread, _, _) = tick()

        self.assertIn(watcher, sread)
        obj_name = path2id(watcher.read())
        client.notify_new_object(self.stations[0], obj_name)
        client.send()

        peer.recv()
        data = peer.packet_queue.pop()
        gizmo = self.stations[1].gizmo_factory.hydrate(data, peer)
        assert gizmo is not None, "gizmo_factory returned None"
        gizmo.process()
        peer.send()

        client.recv()
        data = client.packet_queue.pop()
        gizmo = self.stations[0].gizmo_factory.hydrate(data, peer)
        assert gizmo is not None, "gizmo_factory returned None"
        self.assertEqual(gizmo.verb, "FETCHOBJECT")
        self.assertEqual(gizmo.payload, obj_name)
        gizmo.process()

        watcher.kill()
