import pyaudio

class AudioAnnouncer(object):
    def __init__(self, freq):
        self.audio = pyaudio.PyAudio()
        self.freq = freq

    def ping(self):
        return None
