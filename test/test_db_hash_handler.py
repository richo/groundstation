import hashlib
from handler_fixture import StationHandlerTestCase

from groundstation.transfer.request_handlers import handle_listdbhash
from groundstation.transfer.response_handlers import handle_terminate
import groundstation.transfer.response as response

from groundstation.proto.db_hash_pb2 import DBHash

class TestHandlerNullDatabase(StationHandlerTestCase):
    def test_handle_dbhash_returns_const_for_empty_db(self):
        # hashlib.sha1().digest()
        null_hash = '\xda9\xa3\xee^kK\r2U\xbf\xef\x95`\x18\x90\xaf\xd8\x07\t'

        self.station.payload = ""
        handle_listdbhash(self.station)

        resp = self.station.stream.pop()
        self.assertIsInstance(resp, response.Response)

        db_hash = DBHash()
        db_hash.ParseFromString(resp.payload)

        self.assertEqual(db_hash.hash, null_hash)
        self.assertEqual(db_hash.prefix, "")


class TestHandlerPopulatedDataBase(StationHandlerTestCase):
    def test_prefixes_work_for_populated_db(self):
        # Create some test data.
        oids = []
        prefixes = ("a", "1c", "eb9")
        for i in xrange(100):
            oid = self.station.station.write("butts %d" % i)
            oids.append(oid)

        oids = sorted(oids)
        hashes = {}
        for prefix in prefixes:
            s = hashlib.sha1()
            for i in oids:
                if i.startswith(prefix):
                    s.update(i)
            hashes[prefix] = s.digest()

        for prefix in prefixes:
            self.station.payload = prefix
            handle_listdbhash(self.station)

            resp = self.station.stream.pop()
            self.assertIsInstance(resp, response.Response)

            db_hash = DBHash()
            db_hash.ParseFromString(resp.payload)

            self.assertEqual(db_hash.hash, hashes[prefix])
            self.assertEqual(db_hash.prefix, prefix)
