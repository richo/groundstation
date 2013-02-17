import unittest

import shutil

from groundstation.objects.root_object import RootObject
from groundstation.objects.update_object import UpdateObject


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

    def create_update_object(self, parents, data):
        return UpdateObject(parents, data)

    def create_root_object(self, gref):
        return RootObject(gref.identifier, gref.channel, "test_protocol")

    def test_create_blob(self):
        blob = self.repo.create_blob("rawr lol butts")
        self.assertTrue(blob in self.repo)
