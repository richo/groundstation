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

    def test_barfs_on_invalid_keys(self):
        self.assertRaises(TypeError, convert_pubkey, crypto_fixture.invalid_pubkey)

    def test_initializes_with_keyset(self):
        adaptor = RSAAdaptor({
            "key1": crypto_fixture.valid_pubkey,
            "key2": crypto_fixture.valid_pubkey,
            "key3": crypto_fixture.valid_pubkey,
            "key4": crypto_fixture.valid_pubkey
            })
        self.assertIsInstance(adaptor, RSAAdaptor)
