import time

from station_fixture import StationTestCase
from groundstation.fs_watcher import FSWatcher


class TestFSNotifcation(StationTestCase):
    def test_fs_notification(self):
        ret = []
        watcher = FSWatcher(self.station.store.object_root)

        @watcher.register_handler
        def handler(event):
            ret.append(event)

        self.station.write("foobarbaz")

        self.station.write("foobarbaz1")

        self.station.write("foobarbaz2")
        self.station.write("foobarbaz2")
        time.sleep(.1)

        self.assertEqual(len(ret), 3)

        watcher.observer.stop()
        watcher.observer.join()
