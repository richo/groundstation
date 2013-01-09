import uuid

from groundstation.proto.gizmo_pb2 import Gizmo
import groundstation.transfer.response

from groundstation.transfer import request_handlers

from groundstation import logger
log = logger.getLogger(__name__)


class InvalidRequest(Exception):
    pass


class Request(object):
    VALID_REQUESTS = {
            "LISTALLOBJECTS": request_handlers.handle_listallobjects,
            "FETCHOBJECT": request_handlers.handle_fetchobject,
    }

    def __init__(self, verb, station=None, stream=None, payload=None, origin=None, remoteId=None):
        self.type = "REQUEST"
        self.id = remoteId or uuid.uuid1()
        self.verb = verb
        self.station = station
        self.stream = stream
        self.payload = payload
        # if origin:
        #     self.origin = uuid.UUID(origin)
        self.origin = origin
        self.validate()

    def _Response(self, *args, **kwargs):
        kwargs['station'] = self.station
        return groundstation.transfer.response.Response(*args, **kwargs)


    @classmethod
    def from_gizmo(klass, gizmo, station, stream):
        log.debug("Hydrating a request from gizmo")
        return klass(gizmo.verb, station, stream, gizmo.payload, gizmo.stationid, remoteId=gizmo.id)

    def SerializeToString(self):
        gizmo = self.station.gizmo_factory.gizmo()
        gizmo.id = str(self.id)
        gizmo.type = Gizmo.REQUEST
        gizmo.verb = self.verb
        if self.payload:
            gizmo.payload = self.payload
        return gizmo.SerializeToString()

    def validate(self):
        if self.verb not in self.VALID_REQUESTS:
            raise Exception("Invalid Request: %s" % (self.verb))

    def process(self):
        self.VALID_REQUESTS[self.verb](self)

    def TERMINATE(self):
        terminate = self._Response(self.id, "TERMINATE", None)
        self.stream.enqueue(terminate)

    # Boilerplate to appease protobuf
    @property
    def payload(self):
        return self._payload
    @payload.setter
    def payload(self, value):
        self._payload = str(value)

