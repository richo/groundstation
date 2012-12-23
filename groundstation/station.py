import os

import pygit2

class Station(object):
    def __init__(self, path):
        if os.path.exists(path):
            self.repo = pygit2.Repository(path)
        else:
            pygit2.init_repository(path, True)
