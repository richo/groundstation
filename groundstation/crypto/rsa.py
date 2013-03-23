import sys
import base64
import struct

from Crypto.PublicKey import RSA


def materialise_exponent(e):
    return eval('0x' + ''.join(['%02X' % struct.unpack('B', x)[0] for x in e]))


def materialise_numeric(n):
    return eval('0x' + ''.join(['%02X' % struct.unpack('B', x)[0] for x in n]))


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

    return RSA.construct((long(exponent), long(numeric)))

class RSAAdaptor(object):
    def __init__(self, keyset):
        """Initialize an RSAAdaptor

        keyset = a dict of identifiers to public keys to test signatures
                 against
        """
        pass
