import groundstation.proto
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

    def __init_from_gizmo__(self, gizmo, station, stream):
        self.id = gizmo.id
        self.station = station
        self.stream = stream
        self.origin = gizmo.stationid
        self.verb = gizmo.verb
        if gizmo.verb in self.PAYLOAD_INITIALISERS:
            self.payload = self.PAYLOAD_INITIALISERS[gizmo.verb](gizmo.payload)
        else:
            self.payload = gizmo.payload

    def _Request(self, *args, **kwargs):
        kwargs['station'] = self.station
        req = groundstation.transfer.request.Request(*args, **kwargs)
        self.station.register_request(req)
        return req

    @classmethod
    def from_gizmo(klass, gizmo, station, stream):
        log.debug("Hydrating a response from gizmo: %s" % (str(gizmo)))
        resp = Response.__new__(Response)
        resp.__init_from_gizmo__(gizmo, station, stream)
        return resp

    def SerializeToString(self):
        gizmo = self.station.gizmo_factory.gizmo()
        gizmo.id = str(self.id)
        gizmo.type = groundstation.proto.gizmo_pb2.Gizmo.RESPONSE
        gizmo.verb = self.verb
        if self.payload:
            gizmo.payload = self.serialize_payload(self.payload)
        return gizmo.SerializeToString()

    @staticmethod
    def serialize_payload(payload):
        if isinstance(payload, groundstation.proto.gizmo_pb2.Gizmo):
            return str(payload.SerializeToString())
        else:
            return payload

    def process(self):
        if self.verb not in self.VALID_RESPONSES:
            raise Exception("Invalid Response verb: %s" % (self.verb))

        self.VALID_RESPONSES[self.verb](self)

    def handle_transfer(self):
        resp = groundstation.proto.response.transfer_pb2.Transfer()
        resp.ParseFromString(self.payl)
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

    def init_transfer(self, payload):
        resp = groundstation.proto.response.transfer_pb2.Transfer()
        resp.type = payload.type
        resp.data = payload.data
        return resp.SerializeToString()

    VALID_RESPONSES = {
            "TRANSFER": handle_transfer,
            "DESCRIBEOBJECTS": handle_describe_objects,
            "TERMINATE": handle_terminate,
    }
    PAYLOAD_INITIALISERS = {
            "TRANSFER": init_transfer
    }
