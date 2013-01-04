from unittest import TestCase

from groundstation.transfer.request import Request

class TestGizmoRequest(TestCase):
    def test_loadable_after_serializing(self):
        gizmo = Request("LISTALLOBJECTS")

    def test_rejects_invalid_verbs(self):
        with self.assertRaises(Exception):
            gizmo = Request("THISWILLNEVERBEAVALIDVERB")

