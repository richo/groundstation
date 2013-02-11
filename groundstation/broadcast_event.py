import uuid

class BroadcastEvent(object):
    def __init__(self):
        self.validate()

    def validate(self):
        return True # Assume that if no validation is specified its all good

    @staticmethod
    def normalize_payload(payload):
        if payload == 'None':
            return None

        try:
            return uuid.UUID(payload)
        except ValueError:
            pass

        return payload
