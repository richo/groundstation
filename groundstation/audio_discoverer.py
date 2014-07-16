import Queue
import groundstation.audio as audio
import quietnet.quietnet as quietnet
import pyaudio

class AudioDiscoverer(object):

    def __init__(self, freq, freq_off, _audio):
        self.audio = _audio
        self.freq = freq
        self.freq_off = freq_off
        self.stream = audio.get_stream(self.audio, input=True, stream_callback=self.append_msg,
                                       frames_per_buffer=audio.FRAMES_PER_BUFFER)
        self.msgs = Queue.Queue(4096)

    def append_msg(self, in_data, frame_count, time_info, status):
        frames = list(quietnet.chunks(quietnet.unpack(in_data), audio.CHUNK))
        for frame in frames:
            if frame and not self.msgs.full():
                self.msgs.put(frame, False)
        return (in_data, pyaudio.paContinue)

    def start(self):
        self.stream.start_stream()

    # Size is a relic of the socket based API, and probably needs to be refactored out
    def recv(self, size=None):
        "Recieve a payload from the underlying audio stream, blocking if necessary"
        item = self.msgs.get(True)
        return item
