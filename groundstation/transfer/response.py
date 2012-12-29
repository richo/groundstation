from groundstation.proto.gizmo_pb2 import Gizmo

from groundstation import logger
log = logger.getLogger(__name__)

import pygit2

class Response(object):
    def __init__(self, response_to, payload, station=None, stream=None):
        self.type = "RESPONSE"
        self.id = response_to
        if payload is not None:
            self.verb = "TRANSFER"
        else:
            self.verb = "TERMINATE"
        self.payload = payload

    @classmethod
    def from_gizmo(klass, gizmo, station, stream):
        return Response(gizmo.id, gizmo.payload)

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
        log.info("Handling reponse for %s" % (str(self)))
