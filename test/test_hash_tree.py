import unittest
import groundstation.transfer.hash_tree as hash_tree


class HashTreeSlicesTest(unittest.TestCase):
    def test_slices(self):
        self.assertEqual(
                hash_tree.slices(3, "1234567890"),
                ["12", "34", "56", "7890"]
                )


class HashTreeTest(unittest.TestCase):
    def test_append(self):
        ht = hash_tree.HashTree(3)
        ht.append("1234567890")
        ht.append("1234567811")
        self.assertTrue(ht.tree["12"]["34"]["56"]["7890"])
        self.assertTrue(ht.tree["12"]["34"]["56"]["7811"])
