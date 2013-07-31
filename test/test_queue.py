import unittest

from groundstation.utils.queue import Queue

class TestQueue(unittest.TestCase):
    def test_trims_fifo(self):
        q = Queue(2)
        q.append(0)
        q.append(1)
        q.append(2)
        self.assertNotIn(0, q)
        self.assertIn(1, q)
        self.assertIn(2, q)

    def test_trims_fifo_dynamically(self):
        q = Queue(10)
        q.append(0)
        q.append(1)
        q.append(2)

        q.size = 2
        self.assertNotIn(0, q)
        self.assertIn(1, q)
        self.assertIn(2, q)
