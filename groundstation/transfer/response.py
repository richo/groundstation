from groundstation.transfer import response_handlers

from groundstation.proto.gizmo_pb2 import Gizmo
import groundstation.transfer.request

from groundstation import logger
log = logger.getLogger(__name__)

import pygit2


class Response(object):
    def __init__(self, response_to, verb, payload, station=None, stream=None, origin=None):
        self.type = "RESPONSE"
        self.id = response_to
        self.station = station
        self.stream = stream
        self.verb = verb
        self.payload = payload
        # if origin:
        #     self.origin = uuid.UUID(origin)
        self.origin = origin

    def _Request(self, *args, **kwargs):
        kwargs['station'] = self.station
        req = groundstation.transfer.request.Request(*args, **kwargs)
        self.station.register_request(req)
        return req

    @classmethod
    def from_gizmo(klass, gizmo, station, stream):
        log.debug("Hydrating a response from gizmo")
        return Response(gizmo.id, gizmo.verb, gizmo.payload, station, stream, gizmo.stationid)

    def SerializeToString(self):
        gizmo = self.station.gizmo_factory.gizmo()
        gizmo.id = str(self.id)
        gizmo.type = Gizmo.RESPONSE
        gizmo.verb = self.verb
        if self.payload:
            gizmo.payload = self.payload
        return gizmo.SerializeToString()

    def process(self):
        if self.verb not in self.VALID_RESPONSES:
            raise Exception("Invalid Response verb: %s" % (self.verb))

        self.VALID_RESPONSES[self.verb](self)

    VALID_RESPONSES = {
            "TRANSFER": response_handlers.handle_transfer,
            "DESCRIBEOBJECTS": response_handlers.handle_describeobjects,
            "DESCRIBECHANNELS": response_handlers.handle_describechannels,
            "TERMINATE": response_handlers.handle_terminate,
    }

    @property
    def payload(self):
        return self._payload
    @payload.setter
    def payload(self, value):
        self._payload = str(value)
