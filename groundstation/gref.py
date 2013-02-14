import os


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

    def remove_tip(self, tip):
        try:
            os.unlink(os.path.join(self.tip_path(tip)))
        except:
            raise
