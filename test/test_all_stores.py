import os

from support import store_fixture
import groundstation.store


class TestGitStore(store_fixture.StoreTestCase):
    storeClass = groundstation.store.git_store.GitStore

    def test_creates_required_dirs(self):
        for d in groundstation.store.git_store.GitStore.required_dirs:
            path = os.path.join(self.path, d)
            self.assertTrue(os.path.exists(path))
            self.assertTrue(os.path.isdir(path))
