from collections import defaultdict


def new_dd():
    return defaultdict(new_dd)


def slices(num, string):
    store = []
    for i in xrange(num):
        store.append(string[0:2])
        string = string[2:]
    store.append(string)
    return store


class HashTree(object):
    """\
    HashTree provides a light way to serialize lists of strings which
    share common prefixes
    """

    def __init__(self, depth):
        self.depth = depth
        self.tree = new_dd()

    def append(self, key):
        values = slices(self.depth, key)
        store = self.tree
        tip = values.pop()
        while values:
            k = values.pop(0)
            store = store[k]
        store[tip] = True
