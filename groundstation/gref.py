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
            os.unlink(os.path.join(self.tip_path(tip)))
        except:
            if not silent:
                raise

    def direct_parents(self, tip):
        """Return all parents of `tip` in the order they're written into the
        object"""
        obj = object_factory.hydrate_object(self.store[tip].data)
        if isinstance(obj, RootObject):
            # Roots can't have parents
            return []
        elif isinstance(obj, UpdateObject):
            return obj.parents
        else:
            raise "Unknown object hydrated %s" % (str(type(obj)))

    def parents(self, tips=None):
        """Return all ancestors of `tip`, in an undefined order"""
        # XXX This will asplode the stack at some point
        parents = set()
        this_iter = (tips or self.tips())
        while this_iter:
            tip = this_iter.pop()
            tips_parents = self.direct_parents(tip)
            parents = parents.union(set(tips_parents))
            this_iter.extend(tips_parents)
        return parents

    def marshall(self):
        """Marshalls the gref into something renderable:
        {
            "thread": An ordered thread of UpdateObjects. Ordering is
                      arbitraryish.
            "roots": The root nodes of this gref.
            "tips": The string names of the tips used to marshall
        }
        """
        thread = []
        root_nodes = []
        visited_nodes = set()
        tips = []

        # TODO Big issues will smash the stack
        def _process(node):
            if node in visited_nodes:
                log.debug("Bailing on visited node: %s" % (node))
                return
            visited_nodes.add(node)

            obj = object_factory.hydrate_object(self.store[node].data)
            if isinstance(obj, RootObject):  # We've found a root
                root_nodes.append(obj)
                return
            for tip in obj.parents:
                _process(tip)
            thread.insert(0, obj)

        for tip in self:
            tips.append(tip)
            log.debug("Descending into %s" % (tip))
            _process(tip)
        return {
                "thread": thread,
                "roots": root_nodes,
                "tips": tips
                }

    def as_dict(self):
        return {
                "channel": self.channel,
                "identifier": self.identifier,
                "node_path": self._node_path
                }
