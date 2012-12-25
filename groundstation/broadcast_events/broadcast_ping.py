import uuid

from groundstation.broadcast_event import BroadcastEvent

class BroadcastPing(BroadcastEvent):
    def __init__(self, data):
        self.payload = self.normalize_payload(data)
        super(BroadcastPing, self).__init__()

    def validate(self):
        assert isinstance(self.payload, uuid.UUID)
