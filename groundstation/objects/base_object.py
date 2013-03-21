import pygit2
from groundstation.utils import oid2hex


class BaseObject(object):
    @property
    def sha1(self):
        if self._sha1:
            return self._sha1
        else:
            self._sha1 = oid2hex(pygit2.hash(self.as_object()))
            return self._sha1

    @sha1.setter
    def sha1(self, value):
        self._sha1 = value
