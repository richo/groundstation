import os
import signal

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

class FSHandler(FileSystemEventHandler):
    def __init__(self, pipe):
        self.pipe = pipe
        super(FSHandler, self).__init__()

    def on_created(self, event):
        if isinstance(event, FileCreatedEvent):
            sent = 0
            data = event.src_path + chr(0)
            data_len = len(data)
            while sent != data_len:
                sent += os.write(self.pipe, data[sent:])


class Watcher(object):
    """Wrapper object to allow for being passed into select()"""
    def __init__(self, pid, pipe):
        self.pid = pid
        self.pipe = pipe

    def fileno(self):
        return self.pipe

    def read(self):
        """Block until we can read a full, comma seperated path out"""
        nul = chr(0)
        buf = ""
        while True:
            c = os.read(self.pipe, 1)
            if c == nul:
                break
            buf += c
        assert len(buf) > 0, "Didn't get any data from pipe"
        return buf

    def kill(self):
        # Use sigkill because we can't risk the race conditions.
        os.kill(self.pid, signal.SIGKILL)



def FSWatcher(path):
    _out, _in = os.pipe()
    _pid = os.fork()
    if _pid > 0:
        return Watcher(_pid, _out)
    elif _pid == 0:
        # Run doesn't create a new thread
        watch(path, _in)
    else:
        raise Exception("fork()")


def watch(path, pipe):
    path = path
    pipe = pipe
    observer = Observer()
    handler = FSHandler(pipe)
    observer.schedule(handler, path=path, recursive=True)
    # Write a null to the pipe so we know we're ready
    os.write(pipe, chr(0))
    observer.run()
