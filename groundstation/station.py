import os
import time

import logger
log = logger.getLogger(__name__)

from user import User, NoSuchUser

from packed_keys import PackedKeys, NoKeysRef
from gizmo_factory import GizmoFactory, InvalidGizmoError
from request_registry import RequestRegistry

import store

import settings

class Station(object):
    def __init__(self, path, identity):
        self.identity = identity
        self.store = store.STORAGE_BACKENDS[settings.STORAGE_BACKEND](path)
        self.gizmo_factory = GizmoFactory(self, identity)
        self.identity_cache = {}
        self.registry = RequestRegistry()
        self.iterators = []

    def register_request(self, request):
        log.debug("NOT Registering request %s" % (str(request.id)))
        if False:
            self.registry.register(request)

    def free_request(self, request):
        log.debug("Freeing request %s" % (str(request.id)))
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

    # Delegate some methods to the store
    def write(self, obj):
        log.info("Writing object to db")
        oid = self.store.create_blob(obj)
        log.info("Wrote object %s" % oid)
        return oid

    def objects(self):
        return self.store.objects()

    def __getitem__(self, key):
        return self.store.__getitem__(key)

    def __contains__(self, item):
        return self.store.__contains__(item)
    # End delegates to store

    def get_user(self, name):
        return User(name, self)

    def get_keys(self, user):
        """Fetch the keys from an object pointed to by $db/users/_name_/keys"""
        try:
            ref = self.store.lookup_reference(user.keys_ref)
            assert ref.oid in self.store, "Invalid user keys ref"
            return PackedKeys(self.store[ref.oid].read_raw())
        except KeyError:
            raise NoKeysRef(user.name)

    def set_keys(self, user, keys):
        """Serialize the keys, then write them out to the db and update the ref"""
        ref = self.store.create_blob(keys.pack())
        try:
            self.store.lookup_reference(user.keys_ref).oid = ref
        except KeyError:
            self.store.create_reference(user.keys_ref, ref)

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
