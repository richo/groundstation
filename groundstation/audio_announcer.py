import audio
import quietnet
import pyaudio

from groundstation import logger
log = logger.getLogger(__name__)


class AudioAnnouncer(object):
    def __init__(self, freq):
        self.audio = pyaudio.PyAudio()
        self.freq = freq
        self.stream = audio.get_stream(self.audio, output=True)

    def ping(self):
        log.info("Broadcasting audio ping")
