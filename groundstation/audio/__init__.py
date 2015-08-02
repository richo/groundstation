import sys

try:
    import pyaudio
except ImportError:
    # FIXME: Nasty hack to work around virtualenv on arm.
    sys.path.append('/usr/lib/python2.7/dist-packages')
    import pyaudio

# Shamelessly stolen directly from quietnet
RATE = 2400
CHANNELS = 1
FRAME_LENGTH = 3
CHUNK = 256
DATASIZE = CHUNK * FRAME_LENGTH
BEACON_TIMEOUT = 1
# FREQUENCY = 6500
FREQUENCY = 440
FREQUENCY_OFF = 880
SIGIL = 123

TONES = {
    0: FREQUENCY_OFF,
    1: FREQUENCY,
    None: 330,
}

FRAMES_PER_BUFFER = CHUNK * 10

FORMAT = pyaudio.paFloat32

p = pyaudio.PyAudio()
audio_singleton = p

def get_stream(a, **kwargs):
    """a: a pyaudio.PyAudio"""
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
    default_args = dict(format=FORMAT, channels=CHANNELS, rate=RATE)
    default_args.update(kwargs)
    return a.open(**default_args)
