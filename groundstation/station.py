import os

import pygit2

import logger
log = logger.getLogger(__name__)

class Station(object):
    def __init__(self, path):
        if os.path.exists(path):
            self.repo = pygit2.Repository(path)
        else:
            log.info("initializing database in %s" % (path))
            pygit2.init_repository(path, True)
