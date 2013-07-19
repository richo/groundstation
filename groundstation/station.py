import os
import time
import hashlib

import logger
log = logger.getLogger(__name__)

from packed_keys import PackedKeys, NoKeysRef
from gizmo_factory import GizmoFactory, InvalidGizmoError
from request_registry import RequestRegistry
from groundstation.gref import Gref
from groundstation.crypto.rsa import RSAAdaptor, RSAPrivateAdaptor

import groundstation.utils

import store

import settings


class NonExistantChannel(Exception):
    pass


class Station(object):
    def __init__(self, path, identity):
        self.identity = identity
        self.store = store.STORAGE_BACKENDS[settings.STORAGE_BACKEND](path)
        self.gizmo_factory = GizmoFactory(self, identity)
        self.identity_cache = {}
        self.registry = RequestRegistry()
        self.iterators = []
        self.deferreds = []

    @staticmethod
    def from_env(identity):
        if "GROUNDSTATION_HOME" in os.environ:
            return Station(os.getenv("GROUNDSTATION_HOME"), identity)
        else:
            station_path = os.path.expanduser("~/.groundstation")
            return Station(station_path, identity)

    def get_crypto_adaptor(self):
        return RSAAdaptor(self.store.get_public_keys())

    def get_private_crypto_adaptor(self, keyname):
        return RSAPrivateAdaptor(self.store.get_private_key(keyname))

    def get_request(self, request_id):
        return self.registry[request_id]

    def register_request(self, request):
        log.debug("Registering request %s" % (str(request.id)))
        self.registry.register(request)

    def free_request(self, request):
        log.debug("Freeing request %s" % (str(request.id)))
        return self.registry.free(request)

    def register_iter(self, iterator):
        log.info("Registering iterator %s" % (repr(iterator)))
        self.iterators.append(iterator())

    def register_deferred(self, deferred):
        log.info("Registering deferred %s" % (repr(deferred)))
        self.deferreds.append(deferred)

    def has_ready_iterators(self):
        return len(self.iterators) > 0

    def has_ready_deferreds(self):
        now = time.time()
        for i in self.deferreds:
            if i.at < now:
                return True
        return False

    def handle_iters(self):
        for i in self.iterators:
            try:
                i.next()
            except StopIteration:
                self.iterators.remove(i)

    def handle_deferreds(self):
        now = time.time()
        new_deferreds = []
        while self.deferreds:
            i = self.deferreds.pop(0)
            if i.at < now:
                i.run()
            else:
                new_deferreds.append(i)
        [self.deferreds.append(i) for i in new_deferreds]

    def channels(self):
        return os.listdir(self.store.gref_path())
        # channels = {}
        # for channel in os.listdir(self.store.gref_path()):
        #     channels["channel"] = Channel(self.store, channel)

    def create_channel(self, channel_name):
        try:
            os.mkdir(os.path.join(self.store.gref_path(), channel_name))
            return True
        except OSError:
            return False

    def grefs(self, channel):
        channel_path = os.path.join(self.store.gref_path(), channel)
        if not groundstation.utils.is_dir(channel_path):
            raise NonExistantChannel()
        grefs = []
        for id in groundstation.utils.find_leaf_dirs(channel_path, True):
            grefs.append(Gref(self.store, channel, id))
        return grefs

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

    def update_gref(self, gref, tips, parents=[]):
        log.debug("updating %s - %s => %s" % (gref.channel, gref.identifier, tips))
        node_path = gref.node_path()
        tip_oids = []
        for tip in tips:
            gref.write_tip(tip.tip, tip.signature)
            tip_oids.append(tip.tip)
        if parents is True:
            parents = gref.parents(tip_oids)
        for parent in parents:
            gref.remove_tip(parent, True)

    def recently_queried(self, identity):
        """CAS the cache status of a given identity.

        Returns False if you should query them."""
        val = str(identity)
        if val not in self.identity_cache:
            self.mark_queried(identity)
            return False
        else:
            if self.identity_cache[val] + settings.DEFAULT_CACHE_LIFETIME > time.time():
                return True
            else:
                self.mark_queried(identity)
                return False

    def mark_queried(self, identity):
        val = str(identity)
        self.identity_cache[val] = time.time()

    def get_hash(self, prefix):
        # TODO This depends heavily on the order that objects() returns
        sha = hashlib.sha1()
        for oid in sorted(self.objects()):
            name = groundstation.utils.oid2hex(oid)
            if name.startswith(prefix):
                sha.update(name)
        return sha.digest()
