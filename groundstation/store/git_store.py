import os
import pygit2

from groundstation.gref import Gref

import groundstation.logger
log = groundstation.logger.getLogger(__name__)

import groundstation.store
from groundstation.utils import oid2hex


class GitStore(object):
    required_dirs = ("rindex", "grefs", "signing_keys", "public_keys")

    def __init__(self, path):
        # TODO path should probably be a resource, ie redis url etc.
        self.path = path
        if not os.path.exists(os.path.join(path, "objects")):
            log.info("initializing database in %s" % (path))
            pygit2.init_repository(path, True)
        self.repo = pygit2.Repository(path)
        self.check_repo_sanity()

    def objects(self):
        return list(self.repo)

    def __getitem__(self, key):
        if unicode(key) not in self.repo:
            raise groundstation.store.NoSuchObject()
        return self.repo[unicode(key)]

    def __contains__(self, item):
        return unicode(item) in self.repo

    def get_public_keys(self):
        keys = {}
        for name in os.listdir(self.public_keys_path()):
            keys[name] = file.read(self.public_keys_path(name))
        return keys

    def lookup_reference(self, ref):
        return self.repo.lookup_reference(ref)

    def write(self, typ, data):
        return oid2hex(self.repo.write(typ, data))

    def create_blob(self, data):
        return self.write(pygit2.GIT_OBJ_BLOB, data)

    def create_reference(self, ref, data):
        return self.repo.create_reference(ref, data)

    def gref(self, channel, identifier):
        return Gref(self, channel, identifier)

    def local_path(self, *to):
        return os.path.join(self.repo.path, *to)

    def gref_path(self):
        return self.local_path("grefs")

    def rindex_path(self, path):
        return self.local_path("reindex", path)

    def signing_keys_path(self, keyname=None):
        paths = ["signing_keys"]
        if keyname:
            paths.append(keyname)
        return self.local_path(*paths)

    def public_keys_path(self):
        return self.local_path("public_keys")

    def check_repo_sanity(self):
        for path in self.required_dirs:
            nr_path = self.local_path(path)
            if not os.path.exists(nr_path):
                os.makedirs(nr_path)
