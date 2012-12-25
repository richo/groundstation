class Response(object):
    def __init__(self, response_to, payload):
        self.type = "RESPONSE"
        self.id = response_to
        if payload is not None:
            self.phase = "TRANSFER"
        else:
            self.phase = "TERMINATE"
        self.payload = payload
