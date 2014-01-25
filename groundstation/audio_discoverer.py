import pyaudio

class AudioDiscoverer(object):

    def __init__(self, freq):
        self.audio = pyaudio.PyAudio()
        self.freq = freq
        # self.stream = p.open(format=FORMAT, channels=options.channels, rate=options.rate,
        #         input=True, frames_per_buffer=frames_per_buffer, stream_callback=callback)

    # Size is a relic of the socket based API, and probably needs to be refactored out
    def recv(self, size=None):
        "Recieve a payload from the underlying audio stream"
        return None
