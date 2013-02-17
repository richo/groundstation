import os
import groundstation.objects.object_factory as object_factory

from groundstation.objects.update_object import UpdateObject
from groundstation.objects.root_object import RootObject

import logger
log = logger.getLogger(__name__)


class Gref(object):
    def __init__(self, store, channel, identifier):
        self.store = store
        self.channel = channel.replace("/", "_")
        self.identifier = identifier
        self._node_path = os.path.join(self.store.gref_path(),
                                 self.channel,
                                 self.identifier)

    def __str__(self):
        return "%s/%s" % (self.channel, self.identifier)

    def exists(self):
        return os.path.exists(self._node_path)

    def tips(self):
        return os.listdir(self._node_path)

    def node_path(self):
        if not self.exists():
            os.makedirs(self._node_path)

        return self._node_path

    def write_tip(self, tip, signature):
        tip_path = self.tip_path(tip)
        open(tip_path, 'a').close()
        fh = open(tip_path, 'r+')
        fh.seek(0)
        fh.write(signature)
        fh.truncate()
        fh.close()

    def tip_path(self, tip):
        return os.path.join(self.node_path(), tip)

    def __iter__(self):
        return os.listdir(self.node_path()).__iter__()

    def remove_tip(self, tip, silent=False):
        try:
            path = os.path.join(self.tip_path(tip))
            log.info("Unlinking tip at %s" % (path))
            os.unlink(path)
        except:
            if not silent:
                raise

    def parents(self, tips=None):
        """Return all ancestors of `tip`, in an undefined order"""
        # XXX This will asplode the stack at some point
        parents = []
        for tip in (tips or self.tips()):
            obj = object_factory.hydrate_object(self.store[tip].data)
            if isinstance(obj, UpdateObject):
                for tip in obj.parents:
                    parents.append(tip)
                    parents.extend(self.parents([tip]))
            elif isinstance(obj, RootObject):
                return []
            else:
                raise "Unknown object hydrated %s" % (str(type(obj)))
        return parents

    def as_dict(self):
        return {
                "channel": self.channel,
                "identifier": self.identifier,
                "node_path": self._node_path
                }
