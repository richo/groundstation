import groundstation.crypto.rsa as rsa

class BaseProtocol(object):
    def __init__(self, station, repo):
        self.station = station
        self.repo = repo
        self._signing_key = None

    @property
    def signing_key(self):
        return self._signing_key

    @signing_key.setter
    def @signing_key(self, name):
        key_path = self.station.store.private_key_path(name)
        self._signing_key = rsa.RSAPrivateAdaptor(key_name)
