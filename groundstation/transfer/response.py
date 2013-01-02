from groundstation.proto.gizmo_pb2 import Gizmo
from groundstation.proto import response_pb2

from groundstation import logger
log = logger.getLogger(__name__)

import pygit2

class Response(object):
    __Request = None
    def __init__(self, response_to, verb, payload, station=None, stream=None, origin=None):
        # Cheat and load this at class definition time
        if not self.__Request:
            req = __import__("groundstation.transfer.request")
            self.__Request = req.transfer.request.Request
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
        req = self.__Request(*args, **kwargs)
        self.station.register_request(req)
        return req

    @classmethod
    def from_gizmo(klass, gizmo, station, stream):
        log.debug("Hydrating a response from gizmo: %s" % (str(gizmo)))
        return Response(gizmo.id, gizmo.verb, gizmo.payload, station, stream, gizmo.stationid)

    def SerializeToString(self):
        gizmo = self.station.gizmo_factory.gizmo()
        g_response = response_pb2.Response()

        gizmo.id = str(self.id)
        gizmo.type = Gizmo.RESPONSE
        g_response.verb = self.verb
        if self.payload:
            g_response.payload = self.serialize_payload(self.payload)

        self.payload = g_response.SerializeToString()
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
        log.info("Wrote object %s" % (repr(ret)))

    def handle_describe_objects(self):
        if not self.payload:
            log.info("station %s sent empty DESCRIVEOBJECTS payload - new database?" % (str(self.origin)))
            return
        for obj in self.payload.split(chr(0)):
            if obj not in self.station.repo:
                request = self._Request("FETCHOBJECT", payload=obj)
                self.stream.enqueue(request)
            else:
                log.debug("Not fetching already present object %s" % (str(obj)))

    def handle_terminate(self):
        log.warn("Recieved unhandled event TERMINATE for request %s"
                % (str(self.id)))

    VALID_RESPONSES = {
            "TRANSFER": handle_transfer,
            "DESCRIBEOBJECTS": handle_describe_objects,
            "TERMINATE": handle_terminate,
    }
