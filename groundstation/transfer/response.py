from groundstation.proto.gizmo_pb2 import Gizmo

class Response(object):
    def __init__(self, response_to, payload):
        self.type = "RESPONSE"
        self.id = response_to
        if payload is not None:
            self.verb = "TRANSFER"
        else:
            self.verb = "TERMINATE"
        self.payload = payload

    def SerializeToString(self):
        gizmo = Gizmo()
        gizmo.id = str(self.id)
        gizmo.type = Gizmo.REQUEST
        gizmo.verb = self.verb
        if self.payload:
            gizmo.payload = self.payload
        return gizmo.SerializeToString()
