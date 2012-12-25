import uuid

VALID_REQUESTS = [
        "LISTALLBJECTS",
        "FETCHOBJECT"
]

class InvalidRequest(Exception):
    pass

class Request(object):
    def __init__(self, request):
        self.type = "REQUEST"
        self.id = uuid.uuid1()
        self.request = request
        self.validate()

    def validate(self):
        if self.request not in VALID_REQUESTS:
            raise "Invalid Request: %s" % (self.request)
