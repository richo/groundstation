import store_fixture
import groundstation.store

from groundstation.gref import Gref

from object_fixture import update_object, root_object


class TestGrefMarshall(store_fixture.StoreTestCase):
    storeClass = groundstation.store.git_store.GitStore

    def test_marshalls_tips(self):
        gref = Gref(self.repo, "testchannel", "test_write_tip")

        objects = []
        root = root_object("test", "test_channel", "test")
        root_oid = self.repo.create_blob(root.as_object())
        for i in xrange(5):
            update = update_object("test %i" % i, [root_oid])
            update_oid = self.repo.create_blob(update.as_object())
            objects.append(update_oid)
            gref.write_tip(update_oid, "")

        marshalled = gref.marshall()

        for i in objects:
            self.assertIn(i, marshalled["tips"])

    def test_marshalls_roots(self):
        gref = Gref(self.repo, "testchannel", "test_write_root")
        roots = []
        for i in xrange(5):
            root = root_object("test", "test_channel", "test%i" % i)
            root_oid = self.repo.create_blob(root.as_object())
            root.sha1 = root_oid
            roots.append(root_oid)
        # Create an update object for valid tip
        update = update_object("test %i" % i, roots)
        update_oid = self.repo.create_blob(update.as_object())
        gref.write_tip(update_oid, "")

        marshalled = gref.marshall()
        root_hashes = [i.sha1 for i in marshalled["roots"]]

        for i in roots:
            self.assertIn(i, root_hashes)
