import pyaudio

# Shamelessly stolen directly from quietnet
RATE = 44100
CHANNELS = 1
FRAME_LENGTH = 3
CHUNK = 256
DATASIZE = CHUNK * FRAME_LENGTH
SIGIL = "00"
BEACON_TIMEOUT = 1
FREQUENCY = 1400

FRAMES_PER_BUFFER = CHUNK * 10

FORMAT = pyaudio.paInt16

p = pyaudio.PyAudio()
audio_singleton = p

def get_stream(a, **kwargs):
    """a: a pyaudio.PyAudio"""
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
    default_args = dict(format=FORMAT, channels=CHANNELS, rate=RATE)
    default_args.update(kwargs)
    return a.open(**default_args)
