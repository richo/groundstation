import os
import select

from station_fixture import StationTestCase
from groundstation.fs_watcher import FSWatcher
from groundstation.utils import path2id


class TestFSNotifcation(StationTestCase):
    def test_fs_notification(self):
        watcher = FSWatcher(self.station.store.object_root)

        _id = self.station.write("foobarbaz")
        ret = watcher.read()
        self.assertEqual(_id, path2id(ret))

        _id = self.station.write("foobarbaz1")
        ret = watcher.read()
        self.assertEqual(_id, path2id(ret))

        _id = self.station.write("foobarbaz2")
        self.station.write("foobarbaz2")
        ret = watcher.read()
        self.assertEqual(_id, path2id(ret))

        watcher.kill()

    def test_selects_sanely(self):
        watcher = FSWatcher(self.station.store.object_root)

        (s_read, s_write, s_exc) = select.select([watcher.pipe], [], [], 0)
        self.assertEqual(len(s_read), 0)

        self.station.write("newdata")
        (s_read, s_write, s_exc) = select.select([watcher.pipe], [], [], 1)
        self.assertEqual(len(s_read), 1)

        watcher.kill()
