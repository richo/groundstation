import uuid

from groundstation.proto.gizmo_pb2 import Gizmo
import groundstation.transfer.request
from groundstation.transfer import notification_handlers

from groundstation import logger
log = logger.getLogger(__name__)


class Notification(object):
    VALID_NOTIFICATIONS = {
            "NEWOBJECT": notification_handlers.handle_newobject
    }

    def __init__(self, verb, station=None, stream=None, payload=None, origin=None, remoteId=None):
        self.type = "NOTIFICATION"
        self.id = remoteId or uuid.uuid1()
        self.verb = verb
        self.station = station
        self.stream = stream
        self.payload = payload
        # if origin:
        #     self.origin = uuid.UUID(origin)
        self.origin = origin
        self.validate()

    def _Request(self, *args, **kwargs):
        kwargs['station'] = self.station
        req = groundstation.transfer.request.Request(*args, **kwargs)
        self.station.register_request(req)
        return req

    @classmethod
    def from_gizmo(klass, gizmo, station, stream):
        log.debug("Hydrating a notification from gizmo")
        return Notification(gizmo.id, gizmo.verb, gizmo.payload, station, stream, gizmo.stationid)

    def SerializeToString(self):
        gizmo = self.station.gizmo_factory.gizmo()
        gizmo.id = str(self.id)
        gizmo.type = Gizmo.RESPONSE
        gizmo.verb = self.verb
        if self.payload:
            gizmo.payload = self.payload
        return gizmo.SerializeToString()

    def process(self):
        self.VALID_NOTIFICATIONS[self.verb](self)

    # Boilerplate to appease protobuf
    @property
    def payload(self):
        return self._payload
    @payload.setter
    def payload(self, value):
        self._payload = str(value)
