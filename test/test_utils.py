import os
import shutil
import unittest
import tempfile
from groundstation import utils


class TestUtilsLeafDirs(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmpdir, "foo", "bar", "baz"))
        os.makedirs(os.path.join(self.tmpdir, "foo", "borp"))
        os.makedirs(os.path.join(self.tmpdir, "foo", "test", "test", "test"))

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_find_leaf_dirs(self):
        leaves = utils.find_leaf_dirs(self.tmpdir)

        self.assertIn(os.path.join(self.tmpdir, "foo", "bar", "baz"), leaves)
        self.assertIn(os.path.join(self.tmpdir, "foo", "borp"), leaves)
        self.assertIn(os.path.join(self.tmpdir, "foo", "test", "test", "test"), leaves)

        self.assertNotIn(os.path.join(self.tmpdir, "foo", "bar"), leaves)
        self.assertNotIn(os.path.join(self.tmpdir, "foo"), leaves)
        self.assertNotIn(os.path.join(self.tmpdir, "foo", "test", "test"), leaves)

    def test_find_leaf_dirs_as_idents(self):
        leaves = utils.find_leaf_dirs(self.tmpdir, True)

        self.assertIn(os.path.join("foo", "bar", "baz"), leaves)
        self.assertIn(os.path.join("foo", "borp"), leaves)
        self.assertIn(os.path.join("foo", "test", "test", "test"), leaves)

        self.assertNotIn(os.path.join("foo", "bar"), leaves)
        self.assertNotIn(os.path.join("foo"), leaves)
        self.assertNotIn(os.path.join("foo", "test", "test"), leaves)

class TestPath2Id(unittest.TestCase):
    def test_path2id(self):
        self.assertEqual(utils.path2id("/long/tail/name/as/asdfasdfasdf"), "asasdfasdfasdf")
