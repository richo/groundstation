import hashlib
import groundstation.utils as utils

import groundstation.proto.db_hash_pb2


def handle_listdbhash(self):
    prefix = self.payload

    hash = self.station.get_hash(prefix)

    db_hash = groundstation.proto.db_hash_pb2.DBHash()
    db_hash.prefix = prefix
    db_hash.hash = hash

    response = self._Response(self.id, "DESCRIBEHASH", db_hash.SerializeToString())
    self.stream.enqueue(response)
    self.TERMINATE()
