import unittest
from Crypto.PublicKey import RSA

import crypto_fixture
from groundstation.crypto.rsa import RSAAdaptor, convert_pubkey


valid_keyset = {
        "valid": crypto_fixture.valid_pubkey
        }


class CryptoRSAAdaptorTestCase(unittest.TestCase):
    def test_converts_pubkey_to_pem(self):
        key = convert_pubkey(crypto_fixture.valid_pubkey)
        self.assertIsInstance(key, RSA._RSAobj)
