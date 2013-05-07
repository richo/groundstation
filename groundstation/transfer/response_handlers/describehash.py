import groundstation.proto.db_hash_pb2


def handle_describehash(self):
    db_hash = groundstation.proto.db_hash_pb2.DBHash()

    db_hash.ParseFromString(self.payload)
    if not self.station.get_hash(db_hash.prefix) == db_hash.hash:
        # Objects are missing. Work out what they are
        request = self._Request("LISTALLOBJECTS", payload=db_hash.prefix)
        self.stream.enqueue(request)
        # We also need to work out how to tell them what we've got. Request-request type?
    self.TERMINATE()
