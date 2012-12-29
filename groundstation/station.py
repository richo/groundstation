import os
import time

import pygit2

import logger
log = logger.getLogger(__name__)

from user import User, NoSuchUser

from packed_keys import PackedKeys, NoKeysRef
from gizmo_factory import GizmoFactory, InvalidGizmoError

import settings

class Station(object):
    def __init__(self, path, identity):
        self.identity = identity
        if not os.path.exists(path):
            log.info("initializing database in %s" % (path))
            pygit2.init_repository(path, True)
        self.repo = pygit2.Repository(path)
        self.gizmo_factory = GizmoFactory(self, identity)
        self.identity_cache = {}

    @staticmethod
    def _build_objects(db, dirname, files):
        cur = os.path.basename(dirname)
        if len(cur) == 2:
            for file in files:
                db.append(u"".join((cur, file)))

    def objects(self):
        db = []
        os.path.walk(os.path.join(self.repo.path, "objects"), self._build_objects, db)
        return db

    def get_user(self, name):
        return User(name, self)

    def get_keys(self, user):
        """Fetch the keys from an object pointed to by $db/users/_name_/keys"""
        try:
            ref = self.repo.lookup_reference(user.keys_ref)
            assert ref.oid in self.repo, "Invalid user keys ref"
            return PackedKeys(self.repo[ref.oid].read_raw())
        except KeyError:
            raise NoKeysRef(user.name)

    def set_keys(self, user, keys):
        """Serialize the keys, then write them out to the db and update the ref"""
        ref = self.repo.create_blob(keys.pack())
        try:
            self.repo.lookup_reference(user.keys_ref).oid = ref
        except KeyError:
            self.repo.create_reference(user.keys_ref, ref)

    def write_object(self, payload):
        return self.repo.create_blob(payload)

    def recently_queried(self, identity):
        """CAS the cache status of a given identity.

        Returns False if you should query them."""
        val = str(identity)
        if val not in self.identity_cache:
            self.identity_cache[identity] = time.time()
            return False
        else:
            if self.identity_cache[identity] + settings.DEFAULT_CACHE_LIFETIME > time.time():
                return True
            else:
                self.identity_cache[identity] = time.time()
                return False
