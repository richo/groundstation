class NoSuchUser(Exception):
    pass

class User(object):
    def __init__(self, name, station):
        self.name = name
        self.station = station
        self.keys_ref = "refs/users/%s/keys" % name

    @property
    def keys(self):
        return self.station.get_keys(self)

    @keys.setter
    def keys(self, keys):
        return self.station.set_keys(self, keys)
