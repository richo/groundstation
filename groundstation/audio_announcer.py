import sys
import groundstation.audio as audio
import quietnet.quietnet as quietnet
import pyaudio

import alltheFSKs.MFSKModulator as modulator
import alltheFSKs.MFSKDemodulator as demodulator

import groundstation.ue_encoder

from groundstation import logger
log = logger.getLogger(__name__)

# TODO Unify this with BroadcastAnnouncer
PING_PAYLOAD = "PING"
ENCODER = groundstation.ue_encoder.UnambiguousEncoder()
DATASIZE = 2048

class AudioAnnouncer(object):
    def __init__(self, freq, freq_off, _audio):
        self.audio = _audio
        self.freq = freq
        self.freq_off = freq_off
        self.stream = audio.get_stream(self.audio, output=True)
        self.ping_buffer = ENCODER.encode("header", map(ord, PING_PAYLOAD))
        self.other_ping = ENCODER.encode("header", (0,) * 4)

    def ping(self):
        self.ping_buffer, self.other_ping = self.other_ping, self.ping_buffer
        log.info("Broadcasting audio ping")
        log.info(repr(self.ping_buffer))
        mod = modulator.MFSKModulator()
        print repr(self.ping_buffer)
        mod.modulate_symbol(self.ping_buffer)
        demod = demodulator.MFSKDemodulator(sample_rate=audio.RATE, callback=lambda i: sys.stdout.write("%s\n" % repr(i)))
        demod.consume(mod.emit_all())

        mod.write_to_stream(self.stream)
