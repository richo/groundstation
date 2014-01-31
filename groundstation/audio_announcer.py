import audio
import quietnet.quietnet as quietnet
import pyaudio

import groundstation.ue_encoder

from groundstation import logger
log = logger.getLogger(__name__)

# TODO Unify this with BroadcastAnnouncer
PING_PAYLOAD = "PING"
ENCODER = groundstation.ue_encoder.UnambiguousEncoder()
DATASIZE = 2048

def make_buffer_from_bit_pattern(pattern, on_freq, off_freq):
    """ Takes a pattern and returns an audio buffer that encodes that pattern """
    # the key's middle value is the bit's value and the left and right bits are the bits before and after
    # the buffers are enveloped to cleanly blend into each other

    last_bit = pattern[-1]
    output_buffer = []
    offset = 0

    for i in range(len(pattern)):
        bit = pattern[i]
        if i < len(pattern) - 1:
            next_bit = pattern[i+1]
        else:
            next_bit = pattern[0]

        freq = on_freq if bit == 1 else off_freq
        tone = quietnet.tone(freq, DATASIZE, offset=offset)
        output_buffer += quietnet.envelope(tone, left=last_bit=='0', right=next_bit=='0')
        offset += DATASIZE
        last_bit = bit

    return quietnet.pack_buffer(output_buffer)

def pack_ascii_to_bitstream(payload):
    # Assume header data
    # Take the encoded ints, walk along them MSB -> LSB, converting to bits
    out = []
    for c in payload:
        for bit in range(8, 0, -1):
            bit -= 1
            value = ord(c) & (1<<bit)
            out.append(1 if value else 0)
    return out



class AudioAnnouncer(object):
    bitstream = pack_ascii_to_bitstream(PING_PAYLOAD)

    def __init__(self, freq):
        self.audio = pyaudio.PyAudio()
        self.freq = freq
        self.stream = audio.get_stream(self.audio, output=True)
        self.ping_buffer = make_buffer_from_bit_pattern(self.bitstream, self.freq, 0)

    def ping(self):
        log.info("Broadcasting audio ping")
        output = "".join(self.ping_buffer)
        self.stream.write(output)
