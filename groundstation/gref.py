import os


class Gref(object):
    def __init__(self, store, channel, identifier):
        self.store = store
        self.channel = channel.replace("/", "_")
        self.identifier = identifier

    def node_path(self):
        node_path = os.path.join(self.store.gref_path(),
                                 self.channel,
                                 self.identifier)
        if not os.path.exists(node_path):
            os.makedirs(node_path)

        return node_path

    def write_tip(self, tip, signature):
        fh = open(self.tip_path(tip), 'w')
        fh.write(signature)
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

