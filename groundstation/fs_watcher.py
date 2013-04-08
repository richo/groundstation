from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent


class FSHandler(FileSystemEventHandler):
    def __init__(self, watcher):
        self.watcher = watcher
        super(FSHandler, self).__init__()

    def on_created(self, event):
        if isinstance(event, FileCreatedEvent):
            for handler in self.watcher.handlers:
                handler(event)


class FSWatcher(object):
    """Watcher for filesystems

    Discards all directory events, since files are the only things we care
    about
    """

    def __init__(self, path, defer=False):
        self.path = path
        self.observer = Observer()
        self._handler = FSHandler(self)

        self.observer.schedule(self._handler, path=self.path, recursive=True)
        self.handlers = []

        if not defer:
            self.start()

    def start(self):
        self.observer.start()

    def register_handler(self, handler):
        self.handlers.append(handler)
