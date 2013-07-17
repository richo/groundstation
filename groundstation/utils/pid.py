import os
import atexit

def register_pidfile(path):
    with open(path, "w") as fh:
        fh.write(str(os.getpid()))

    @atexit.register
    def _cleanup():
        os.unlink(path)
