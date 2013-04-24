"""Groundstation's RSA module

We make sweeping assumptions about how we can verify data, namely that we can
ignore hashing algorithms and length extension attacks. Where it's reasonable
we assert that you not only have a 40 character SHA1 hash, but also one that
points to a valid object
"""

import sys
import base64
import struct

from Crypto.PublicKey import RSA


def materialise_exponent(e):
    return int(''.join(['%02X' % struct.unpack('B', x)[0] for x in e]), 16)


def materialise_numeric(n):
    return int(''.join(['%02X' % struct.unpack('B', x)[0] for x in n]), 16)


def convert_pubkey(key):
    # get the second field from the public key file.
    # import pdb; pdb.set_trace()
    keydata = base64.b64decode(key.split(None)[1])

    parts = []
    while keydata:
        # read the length of the data
        dlen = struct.unpack('>I', keydata[:4])[0]

        # read in <length> bytes
        data, keydata = keydata[4:dlen+4], keydata[4+dlen:]

        parts.append(data)
    exponent = materialise_exponent(parts[1])
    numeric = materialise_numeric(parts[2])

    return RSA.construct((long(numeric), long(exponent)))


def convert_privkey(key):
    pkey = RSA.importKey(key)
    assert pkey.has_private()
    return pkey


class RSAAdaptor(object):
    def __init__(self, keyset):
        """Initialize an RSAAdaptor

        keyset = a dict of identifiers to public keys to test signatures
                 against
        """
        self.keyset = self._render_keyset(keyset)

    def verify(self, data, signature):
        assert len(data) == 40, "We only sign sha1 hashes"
        for keyname in self.keyset:
            key = self.keyset[keyname]
            if key.verify(str(data), signature):
                return keyname
        return False

    def _render_keyset(self, keyset):
        return {i: convert_pubkey(keyset[i]) for i in keyset}


class RSAPrivateAdaptor(object):
    def __init__(self, key):
        self.key = convert_privkey(key)

    def sign(self, data):
        assert len(data) == 40, "We only sign sha1 hashes"
        return self.key.sign(data, None)
