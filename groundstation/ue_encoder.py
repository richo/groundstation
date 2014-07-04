

# Actually generated with an internal hamming distance of 3, isolation of 2
HAMMING_WEIGHT = 1
DEFAULT_HEADER_CODE = (0, 41)
DEFAULT_MESSAGE_CODE = (54, 31)

class Code(object):
    def __init__(self, code, hamming_weight):
        # Naively assume that all codes are binary
        assert len(code) == 2, "Non binary code"
        self.code = code
        self.lookup_tables = self.setup_lookup_tables(code, hamming_weight)

    def lookup(self, k):
        return self.lookup_tables[k]

    @staticmethod
    def setup_lookup_tables(code, hamming_weight):
        lookup = {}
        if hamming_weight != 1:
            raise Exception("Don't really have a good story for >1 hamming weights right now")


        for value, codepoint in enumerate(code):
            # Insert the raw keys
            lookup[codepoint] = value

            # Setup a lookup for the hammed keys
            for weight in range(hamming_weight):
                for bit in range(0,8):
                    lookup[codepoint ^ 1 << bit] = value
        return lookup


DEFAULT_LOOKUP = {
        "message": Code(DEFAULT_MESSAGE_CODE, 1),
        "header": Code(DEFAULT_HEADER_CODE, 1)
        }

class UnknownCodeCategory(Exception):
    pass


def chunks(length, buf):
    i = 0
    buf_length = len(buf)
    while i < buf_length:
        yield buf[i:i+length]
        i+=length

class UnambiguousEncoder(object):
    def __init__(self, codes=DEFAULT_LOOKUP):
        self.codes = codes

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
                val = code.code[idx]
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
                if code.lookup(byt):
                    this |= (1 << bit)
                bit += 1
            out.append(this)

        return out
