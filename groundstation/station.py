import os
import time

import pygit2

import logger
log = logger.getLogger(__name__)

from user import User, NoSuchUser

from packed_keys import PackedKeys, NoKeysRef
from gizmo_factory import GizmoFactory, InvalidGizmoError
from request_registry import RequestRegistry

import settings

class Station(object):
    def __init__(self, path, identity):
        self.identity = identity
        if not os.path.exists(os.path.join(path, "objects")):
            log.info("initializing database in %s" % (path))
            pygit2.init_repository(path, True)
        self.repo = pygit2.Repository(path)
        self.gizmo_factory = GizmoFactory(self, identity)
        self.identity_cache = {}
        self.registry = RequestRegistry()
        self.iterators = []

    def register_request(self, request):
        log.info("NOT Registering request %s" % (str(request.requestid)))
        if False:
            self.registry.register(request)

    def free_request(self, request):
        log.info("Freeing request %s" % (str(request.requestid)))
        self.registry.free(request)

    def register_iter(self, iterator):
        log.info("Registering iterator %s" % (repr(iterator)))
        self.iterators.append(iterator())

    def has_ready_iterators(self):
        return len(self.iterators) > 0

    def handle_iters(self):
        for i in self.iterators:
            try:
                i.next()
            except StopIteration:
                self.iterators.remove(i)

    def objects(self):
        return list(self.repo)

    def __getitem__(self, key):
        return self.repo[unicode(key)]

    def __contains__(self, item):
        return unicode(item) in self.repo

    def get_user(self, name):
        return User(name, self)

    def get_keys(self, user):
        """Fetch the keys from an object pointed to by $db/users/_name_/keys"""
        try:
            ref = self.repo.lookup_reference(user.keys_ref)
            assert ref.oid in self.repo, "Invalid user keys ref"
            return PackedKeys(self[ref.oid].read_raw())
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
