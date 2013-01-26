import unittest

import shutil


def random_path():
    # TODO
    return "/tmp/groundstation"


class StoreTestCase(unittest.TestCase):
    storeClass = None

    def setUp(self):
        self.path = random_path()
        self.repo = self.storeClass(self.path)

    def tearDown(self):
        shutil.rmtree(self.path)

    def test_create_blob(self):
        blob = self.repo.create_blob("rawr lol butts")
        self.assertTrue(blob in self.repo)
