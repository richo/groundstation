import unittest
import groundstation.transfer.hash_tree as hash_tree


class HashTreeSlicesTest(unittest.TestCase):
    def test_slices(self):
        self.assertEqual(
                hash_tree.slices(3, "1234567890"),
                ["12", "34", "56", "7890"]
                )
