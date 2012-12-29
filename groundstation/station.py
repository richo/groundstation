import os

import pygit2

import logger
log = logger.getLogger(__name__)

from user import User, NoSuchUser

from packed_keys import PackedKeys, NoKeysRef

class Station(object):
    def __init__(self, path):
        if os.path.exists(path):
            self.repo = pygit2.Repository(path)
        else:
            log.info("initializing database in %s" % (path))
            pygit2.init_repository(path, True)

    @staticmethod
    def _build_objects(db, dirname, files):
        cur = os.path.basename(dirname)
        if len(cur) == 2:
            for file in files:
                db.append(u"".join((cur, file)))

    def objects(self):
        db = []
        os.path.walk(os.path.join(self.repo.path, "objects"), self._build_objects, db)
        return db

    def get_user(self, name):
        return User(name, self)

    def get_keys(self, user):
        """Fetch the keys from an object pointed to by $db/users/_name_/keys"""
        try:
            ref = self.repo.lookup_reference(user.keys_ref)
            assert ref.oid in self.repo, "Invalid user keys ref"
            return PackedKeys(self.repo[ref.oid].read_raw())
        except KeyError:
            raise NoKeysRef(user.name)

    def set_keys(self, user, keys):
        """Serialize the keys, then write them out to the db and update the ref"""
        ref = self.repo.create_blob(keys.pack())
        try:
            self.repo.lookup_reference(user.keys_ref).oid = ref
        except KeyError:
            self.repo.create_reference(user.keys_ref, ref)

