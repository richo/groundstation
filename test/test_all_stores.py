import store_fixture
import groundstation.store


class TestGitStore(store_fixture.StoreTestCase):
    storeClass = groundstation.store.git_store.GitStore
