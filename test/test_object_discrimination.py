import unittest

import groundstation.objects.object_factory as object_factory

from groundstation.objects.base_object_pb2 import BaseObject, \
    ROOT as TYPE_ROOT, \
    UPDATE as TYPE_UPDATE, \
    UNSET as TYPE_UNSET
from groundstation.objects.root_object_pb2 import RootObject
from groundstation.objects.update_object_pb2 import UpdateObject


def new_root_object(weak):
    root = RootObject()
    root.id = "butts"
    root.channel = "butts"
    root.protocol = "butts"
    if not weak:
        root.type = TYPE_ROOT
    return root


def new_update_object(weak, parents=[]):
    update = UpdateObject()
    update.parents.extend(parents)
    update.data = "butts"
    if not weak:
        update.type = TYPE_UPDATE
    return update


class TypeOfTestCase(unittest.TestCase):
    def test_strongly_typed_root(self):
        root_str = new_root_object(False).SerializeToString()
        self.assertEqual(object_factory.type_of(root_str), TYPE_ROOT)

    def test_weakly_typed_root(self):
        root_str = new_root_object(True).SerializeToString()
        self.assertEqual(object_factory.type_of(root_str), TYPE_UNSET)

    def test_strongly_typed_update(self):
        update_str = new_update_object(False).SerializeToString()
        self.assertEqual(object_factory.type_of(update_str), TYPE_UPDATE)

    def test_weakly_typed_update(self):
        update_str = new_update_object(True).SerializeToString()
        self.assertEqual(object_factory.type_of(update_str), TYPE_UNSET)
