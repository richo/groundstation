import unittest
import groundstation.objects.object_factory as object_factory
from groundstation.objects.root_object import RootObject
from groundstation.objects.update_object import UpdateObject


class TestRootObject(unittest.TestCase):
    def test_hydrate_root_object(self):
        root = RootObject(
                "test_object",
                "richo@psych0tik.net:groundstation/tests",
                "richo@psych0tik.net:groundstation/testcase"
            )
        hydrated_root = object_factory.hydrate_object(root.as_object())
        self.assertTrue(isinstance(hydrated_root, RootObject))

class TestUpdateObject(unittest.TestCase):
    def test_hydate_update_with_1_parent(self):
        update = UpdateObject(
                ["d41e2dadaf624319518a9dfa8ef4cb0dde055b5c"],
                "Lol I r update data"
            )
        hydrated_update = object_factory.hydrate_object(update.as_object())
        self.assertTrue(isinstance(hydrated_update, UpdateObject))

    def test_hydate_update_with_2_parent(self):
        update = UpdateObject(
                ["d41e2dadaf624319518a9dfa8ef4cb0dde055b5c",
                 "d41e2dadaf624319518a9dfa8ef4cb0dde055bff"],
                "Lol I r update data"
            )
        hydrated_update = object_factory.hydrate_object(update.as_object())
        self.assertTrue(isinstance(hydrated_update, UpdateObject))
