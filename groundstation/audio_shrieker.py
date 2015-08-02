import groundstation.audio as audio

import base64
import struct

from quietnet import psk
from quietnet import options
from quietnet import quietnet as quietnet
from quietnet.send import send_bytes

import time

from groundstation import logger
log = logger.getLogger(__name__)

def make_buffer_from_bit_pattern(pattern, on_freq, off_freq):
    last_bit = pattern[-1]
    output_buffer = []
    offset = 0

    for i in range(len(pattern)):
        bit = pattern[i]
        if i < len(pattern) - 1:
            next_bit = pattern[i+1]
        else:
            next_bit = pattern[0]

        freq = on_freq if bit == '1' else off_freq
        tone = quietnet.tone(freq, options.datasize, offset=offset)
        output_buffer += quietnet.envelope(tone, left=last_bit=='0', right=next_bit=='0')
        offset += options.datasize
        last_bit = bit

    return quietnet.pack_buffer(output_buffer)

def convert_message_to_bits(msg):
    bits = []
    for c in map(ord, msg):
        for i in range(8, 0, -1):
            i -= 1
            bits.append(1 if c & (1 << i) else 0)
    return bits

class AudioShrieker(object):
    def __init__(self, tones, _audio):
        self.audio = _audio
        self.tones = tones
        self.stream = audio.get_stream(self.audio, output=True)

    def send(self, message):
        bits = convert_message_to_bits(message, self.tones)
        for bit in bits:
            pattern = psk.encode([bit], options.sigil)
            buffer = make_buffer_from_bit_pattern(pattern, options.freq, 0)
            self.stream.write(''.join(buffer))
            time.sleep(0.2)

    def shriek(self, station):
        log.info("Sending the contents of station: %s" % (repr(station)))
        while True:
            for name in station.objects():
                encoded = base64.b64encode(station[name])
                length = len(encoded)
                log.info("Yelling %s (%d bytes)" % (name, length))
                # Use a really sketchy scheme:
                # Set the high bit on length messages, leave it low on base64 transmissions (Since they're ascii)
                # Only use the lower 4 bits to make the math easier
                # always send in 4 messages, eg, if you've got messages longer than 64k you're toast
                header_bytes = map(ord, struct.pack(">h", length))
                header_bytes = [
                        (header_bytes[0] & 0xf),
                        (header_bytes[0] >> 4 & 0xf),
                        (header_bytes[1] & 0xf),
                        (header_bytes[1] >> 4 & 0xf),
                ]
                header_bytes = map(lambda x: x | 0b10000000, header_bytes)
                # print repr(map(bin, header_bytes))
                header_bytes = map(chr, header_bytes)

                send_bytes(header_bytes, self.tones)
                log.info("Sent header for %s" % name)
                send_bytes(encoded, self.tones)
