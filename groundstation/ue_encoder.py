

DEFAULT_HEADER_CODE = (0, 41)
DEFAULT_MESSAGE_CODE = (54, 31)

DEFAULT_LOOKUP = {
        "message": DEFAULT_MESSAGE_CODE,
        "header": DEFAULT_HEADER_CODE
        }

class UnknownCodeCategory(Exception):
    pass


def lookup(code, key):
    """Naive, doesn't know about hamming"""
    return code.index(key)

def chunks(length, buf):
    i = 0
    buf_length = len(buf)
    while i < buf_length:
        yield buf[i:i+length]
        i+=length

class UnambiguousEncoder(object):
    def __init__(self, codes=DEFAULT_LOOKUP):
        self.codes = codes

        # Naively assume that all codes are binary
        # Check out naieve assumption
        for name, mapp in self.codes.items():
            assert len(mapp) == 2, "Non binary code"

    def encode(self, cat, buf):
        """ Encodes from LSB"""

        if cat not in self.codes:
            raise UnknownCodeCategory("Unknown code category: %s" % cat)
        code = self.codes[cat]

        out = []
        bit = 1
        for i in buf:
            # Map the bits onto the binary code
            for bit in range(8):
                f = i & (1 << bit)
                idx = 1 if f else 0
                val = code[idx]
                out.append(val)

        return out

    def decode(self, cat, buf):
        if cat not in self.codes:
            raise UnknownCodeCategory("Unknown code category: %s" % cat)
        code = self.codes[cat]

        out = []
        values = chunks(8, buf)

        # Slice off 8 byte chunks because we're encoding from LSB
        for chunk in values:
            bit = 0
            this = 0
            for byt in chunk:
                if lookup(code, byt):
                    this |= (1 << bit)
                bit += 1
            out.append(this)

        return out
