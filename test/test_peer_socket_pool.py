import unittest

from peer_socket_pool_fixture import MockPeer
from groundstation.peer_socket_pool import PeerSocketPool


class TestPeerSocketPool(unittest.TestCase):
    def test_add_remove(self):
        pool = PeerSocketPool()
        peer = MockPeer('127.0.0.1')

        pool.append(peer)
        pool.remove(peer)

        self.assertEqual(0, len(pool))

    def test_throws_error_on_remove_nonexistant_peer(self):
        pool = PeerSocketPool()
        peer = MockPeer('127.0.0.1')

        self.assertRaises(AttributeError, pool.remove, peer)

    def test_safe_multiple_removes(self):
        pool = PeerSocketPool()
        peer = MockPeer('127.0.0.1')

        pool.append(peer)
        pool.remove(peer)
        self.assertEqual(0, len(pool))
        pool.remove(peer)
        self.assertEqual(0, len(pool))

    def test_raises_after_purge(self):
        pool = PeerSocketPool()
        peer = MockPeer('127.0.0.1')

        pool.append(peer)
        pool.remove(peer)
        self.assertEqual(0, len(pool))
        pool.remove(peer)
        self.assertEqual(0, len(pool))

        pool.purge(peer.peer)
        self.assertRaises(AttributeError, pool.remove, peer)
