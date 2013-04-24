import groundstation.transfer.request
import groundstation.proto.object_list_pb2

import groundstation.utils

from groundstation import settings
from groundstation import logger
log = logger.getLogger(__name__)


def handle_listallobjects(self):
    if not self.station.recently_queried(self.origin):
        log.info("%s not up to date, issuing LISTALLOBJECTS" % (self.origin))
        #                                                                      Pass in the station for gizmo_factory in the constructor
        listobjects = groundstation.transfer.request.Request("LISTALLOBJECTS", station=self.station, stream=self.stream)
        self.station.register_request(listobjects)
        self.stream.enqueue(listobjects)
    else:
        log.info("object cache for %s still valid" % (self.origin))
    log.info("Handling LISTALLOBJECTS")
    payload = [groundstation.utils.oid2hex(i) for i in self.station.objects()]
    if len(payload) > settings.LISTALLOBJECTS_CHUNK_THRESHOLD:
        log.info("Lots of objects to send, registering an iterator")

        @self.station.register_iter
        def iterator():
            for chunk in groundstation.utils.chunks(payload, settings.LISTALLOBJECTS_CHUNK_THRESHOLD):
                this_chunk = groundstation.proto.object_list_pb2.ObjectList()
                for obj in chunk:
                    this_chunk.objectname.append(obj)
                log.info("Sending %i object descriptions" % (len(chunk)))
                response = self._Response(self.id, "DESCRIBEOBJECTS", this_chunk.SerializeToString())
                self.stream.enqueue(response)
                yield
            self.TERMINATE()

    else:
        log.info("Sending %i object descriptions" % (len(payload)))
        chunk = groundstation.proto.object_list_pb2.ObjectList()
        chunk.objectname.extend(payload)
        response = self._Response(self.id, "DESCRIBEOBJECTS",
                                chunk.SerializeToString())
        self.stream.enqueue(response)
        self.TERMINATE()
