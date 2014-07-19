import Queue
import groundstation.audio as audio
import quietnet.quietnet as quietnet
import pyaudio
import StringIO
import scipy.io.wavfile as wav
import numpy as np

import alltheFSKs.MFSKDemodulator as demodulator

class AudioDiscoverer(object):

    def __init__(self, freq, freq_off, _audio):
        self.audio = _audio
        self.freq = freq
        self.freq_off = freq_off
        self.stream = audio.get_stream(self.audio, input=True, stream_callback=self.append_msg,
                                       frames_per_buffer=audio.FRAMES_PER_BUFFER)
        self.demod = demodulator.MFSKDemodulator(sample_rate=audio.RATE, callback=self.symbol_callback)
        self.msgs = Queue.Queue(4096)

    def append_msg(self, in_data, frame_count, time_info, status):
        data = np.fromstring(in_data, 'Float32');

        self.demod.consume(data)

        return (in_data, pyaudio.paContinue)

    def start(self):
        self.stream.start_stream()

    # Size is a relic of the socket based API, and probably needs to be refactored out
    def recv(self, size=None):
        "Recieve a payload from the underlying audio stream, blocking if necessary"
        item = self.msgs.get(True)
        return item

    def symbol_callback(self, data):
        print "-> %s" % (repr(data))
