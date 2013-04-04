import store_fixture
import groundstation.store

from groundstation.gref import Gref, valid_path

class TestGitGref(store_fixture.StoreTestCase):
    storeClass = groundstation.store.git_store.GitStore

    def test_write_tip(self):
        gref = Gref(self.repo, "testchannel", "test_write_tip")
        gref.write_tip("foobarbaz", "")
        self.assertEqual(list(gref), ["foobarbaz"])

    def test_remove_tip(self):
        gref = Gref(self.repo, "testchannel", "test_write_tip")
        gref.write_tip("foobarbaz", "")
        gref.write_tip("lulzbutts", "")
        gref.write_tip("buttslols", "")

        gref.remove_tip("lulzbutts")

        self.assertTrue("foobarbaz" in list(gref))
        self.assertTrue("buttslols" in list(gref))
        self.assertFalse("lulzbutts" in list(gref))

    def test_parents(self):
        gref = Gref(self.repo, "testchannel", "test_write_tip")
        root = self.create_root_object(gref)
        current = root
        parents = []
        for i in xrange(10):
            oid = self.repo.create_blob(current.as_object())
            parents.append(oid)
            current = self.create_update_object([oid], "lol data")
        else:
            oid = self.repo.create_blob(current.as_object())
        gref.write_tip(oid, "")
        our_parents = gref.parents()
        for parent in our_parents:
            self.assertIn(parent, parents)

    def test_get_signature(self):
        gref = Gref(self.repo, "testchannel", "test_get_signature")
        root = self.create_root_object(gref)
        oid = self.repo.create_blob(root.as_object())

        signature = (17**23,)
        gref.write_tip(oid, signature)
        self.assertEqual(signature, gref.get_signature(oid))

    def test_direct_parents(self):
        gref = Gref(self.repo, "testchannel", "test_write_tip")
        root = self.create_root_object(gref)
        root_oid = self.repo.create_blob(root.as_object())

        first_tier = []
        for i in xrange(5):
            obj = self.create_update_object([root_oid], "test_%i")
            oid = self.repo.create_blob(obj.as_object())
            first_tier.append(oid)

        final = self.create_update_object(first_tier, "final object")
        final_oid = self.repo.create_blob(final.as_object())

        gref.write_tip(final_oid, "")
        self.assertEqual(gref.direct_parents(final_oid), first_tier)

    def test_valid_path_works(self):
        self.assertTrue(valid_path("asdf"))
        self.assertTrue(valid_path("asdf/foo"))
        self.assertFalse(valid_path("../asdf/asdfasdf"))
        self.assertFalse(valid_path("././asdf/asdfasdf"))
        self.assertFalse(valid_path("asdf/../asdfasdf"))

    def test_raises_on_suspicious_path(self):
        self.assertRaises(AssertionError, Gref, self.repo, "testchannel", "test_write_tip/../hax")
        self.assertRaises(AssertionError, Gref, self.repo, "testchannel", ".")
        self.assertRaises(AssertionError, Gref, self.repo, "testchannel", "..")
