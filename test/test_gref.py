import store_fixture
import groundstation.store

from groundstation.gref import Gref


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
