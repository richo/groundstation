import unittest
from Crypto.PublicKey import RSA

from support import crypto_fixture
from groundstation.crypto.rsa import RSAAdaptor, RSAPrivateAdaptor
from groundstation.crypto.rsa import convert_privkey, convert_pubkey
from groundstation.crypto.rsa import materialise_exponent, materialise_numeric


valid_keyset = {
        "valid": crypto_fixture.valid_pubkey
        }


class CryptoRSAAdaptorTestCase(unittest.TestCase):
    def test_converts_pubkey_to_pem(self):
        key = convert_pubkey(crypto_fixture.valid_pubkey)
        self.assertIsInstance(key, RSA._RSAobj)
        self.assertFalse(key.has_private())

    def test_convertes_privkey_to_pem(self):
        key = convert_privkey(crypto_fixture.valid_key)
        self.assertIsInstance(key, RSA._RSAobj)
        self.assertTrue(key.has_private())

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

    def test_signs_data(self):
        adaptor = RSAPrivateAdaptor(crypto_fixture.valid_key)
        signature = adaptor.sign(crypto_fixture.sample_data)
        self.assertEqual(signature,
                crypto_fixture.signatures["sample_data"]["valid_key"])

    def test_verifies_data(self):
        adaptor = RSAAdaptor({"key1": crypto_fixture.valid_pubkey})
        self.assertEqual("key1", adaptor.verify(
                crypto_fixture.sample_data,
                crypto_fixture.signatures["sample_data"]["valid_key"]
                ))

    def test_returns_false_for_unverified_data(self):
        adaptor = RSAAdaptor({"key1": crypto_fixture.passphrase_pubkey})
        self.assertFalse(adaptor.verify(
                crypto_fixture.sample_data,
                crypto_fixture.signatures["sample_data"]["valid_key"]
                ))

    def test_materialise_helpers(self):
        self.assertEqual(crypto_fixture.materialize_out,
                materialise_exponent(crypto_fixture.materialize_in))
        self.assertEqual(crypto_fixture.materialize_out,
                materialise_numeric(crypto_fixture.materialize_in))
