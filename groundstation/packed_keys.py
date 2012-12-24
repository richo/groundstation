class NoKeysRef(Exception):
    pass

class PackedKeys(object):
    def __init__(self, data):
        """Represents a set of keys packed in the database. Returns an object
        that quacks like a list full of Key objects"""
        pass

    def pack(self):
        """Returns a packed (pickled) representation of internal state, suitable for packing as a blob"""
        pass
