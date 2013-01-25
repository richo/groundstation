import os
import pygit2

import groundstation.logger
log = groundstation.logger.getLogger(__name__)

class GitStore(object):
    def __init__(self, path):
        # TODO path should probably be a resource, ie redis url etc.
        if not os.path.exists(os.path.join(path, "objects")):
            log.info("initializing database in %s" % (path))
            pygit2.init_repository(path, True)
        self.repo = pygit2.Repository(path)

    def objects(self):
        return list(self.repo)

    def __getitem__(self, key):
        return self.repo[unicode(key)]

    def __contains__(self, item):
        return unicode(item) in self.repo

    def lookup_reference(self, ref):
        return self.repo.lookup_reference(ref)

    def write(self, typ, data):
        self.repo.write(typ, data)

    def create_blob(self, data):
        return self.repo.create_blob(data)

    def create_reference(self, ref, data):
        return self.repo.create_reference(ref, data)
