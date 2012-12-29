from proto.gizmo_pb2 import Gizmo
from transfer.request import Request
from transfer.response import Response
class GizmoFactory(object):
    builders = {
            Gizmo.REQUEST: Request,
            Gizmo.RESPONSE: Response
    }
    def __init__(self, station):
        self.station = station

    def hydrate(self, data, stream):
        gizmo = Gizmo.ParseFromString(data)
        try:
            self.builders[gizmo.type](gizmo, self.station, stream)
        except KeyError:
            raise Exception("Invalid message type")
