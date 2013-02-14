import store_fixture
import groundstation.store

from groundstation.gref import Gref


class TestGitGref(store_fixture.StoreTestCase):
    storeClass = groundstation.store.git_store.GitStore

    def test_write_tip(self):
        gref = Gref(self.repo, "testchannel", "test_write_tip")
        gref.write_tip("foobarbaz", "")
        self.assertEqual(list(gref), ["foobarbaz"])
