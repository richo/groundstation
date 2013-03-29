from proto.gizmo_pb2 import Gizmo
from google.protobuf.message import DecodeError
from transfer.request import Request
from transfer.response import Response
from transfer.notification import Notification

import groundstation.logger
log = groundstation.logger.getLogger(__name__)

class GizmoFactory(object):
    builders = {
            Gizmo.REQUEST: Request,
            Gizmo.RESPONSE: Response,
            Gizmo.NOTIFICATION: Notification
    }
    def __init__(self, station, identity):
        self.station = station
        self.identity = identity

    def gizmo(self):
        gizmo = Gizmo()
        gizmo.stationid = self.identity.name
        return gizmo

    def hydrate(self, data, stream):
        log.debug("Attempting to hydrate a Gizmo: %i bytes" % (len(data)))
        gizmo = Gizmo()
        try:
            gizmo.ParseFromString(data)
        except DecodeError:
            raise InvalidGizmoError("Couldn't decode gizmo")
        try:
            return self.builders[gizmo.type].from_gizmo(gizmo, self.station, stream)
        except KeyError:
            raise Exception("Invalid message type")

class InvalidGizmoError(Exception):
    def __init__(self, msg):
        log.warn(msg)
        super(InvalidGizmoError, self).__init__(self)
