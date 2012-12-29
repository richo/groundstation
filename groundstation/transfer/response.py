from groundstation.proto.gizmo_pb2 import Gizmo

from groundstation import logger
log = logger.getLogger(__name__)

import pygit2

class Response(object):
    _Request = None
    def __init__(self, response_to, verb, payload, station=None, stream=None):
        # Cheat and load this at class definition time
        if not self._Request:
            req = __import__("groundstation.transfer.request")
            self._Request = req.transfer.request.Request
        self.type = "RESPONSE"
        self.id = response_to
        self.station = station
        self.stream = stream
        self.verb = verb
        self.payload = payload

    @classmethod
    def from_gizmo(klass, gizmo, station, stream):
        log.debug("Hydrating a response from gizmo: %s" % (str(gizmo)))
        return Response(gizmo.id, gizmo.verb, gizmo.payload, station, stream)

    def SerializeToString(self):
        gizmo = Gizmo()
        gizmo.id = str(self.id)
        gizmo.type = Gizmo.RESPONSE
        gizmo.verb = self.verb
        if self.payload:
            gizmo.payload = self.serialize_payload(self.payload)
        return gizmo.SerializeToString()

    @staticmethod
    def serialize_payload(payload):
        if isinstance(payload, pygit2.Blob):
            return payload.data
        else:
            return payload

    def process(self):
        if self.verb not in self.VALID_RESPONSES:
            raise Exception("Invalid Response verb: %s" % (self.verb))

        self.VALID_RESPONSES[self.verb](self)

    def handle_transfer(self):
        log.info("Handling TRANSFER of %s" % (self.payload))
        ret = self.station.write_object(self.payload)
        log.info("Wrote object %s" % (str(ret)))

    def handle_describe_objects(self):
        for obj in self.payload.split(chr(0)):
            if obj not in self.station.repo:
                request = self._Request("FETCHOBJECT", payload=obj)
                self.stream.enqueue(request)

    def handle_terminate(self):
        log.warn("queing a request of all objects- loop incoming!")
        self.stream.enqueue(self._Request("LISTALLOBJECTS"))
        log.warn("Recieved unhandled event TERMINATE for request %s"
                % (str(self.id)))

    VALID_RESPONSES = {
            "TRANSFER": handle_transfer,
            "DESCRIBEOBJECTS": handle_describe_objects,
            "TERMINATE": handle_terminate,
    }
