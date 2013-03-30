import random

class MockPeer(object):
    def __init__(self, peer):
        self.peer = (peer, random.randint(0, 65535))
