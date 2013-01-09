import groundstation.transfer.request

from groundstation import settings
from groundstation import logger
log = logger.getLogger(__name__)


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def handle_listallobjects(self):
    if not self.station.recently_queried(self.origin):
        log.info("%s not up to date, issuing LISTALLOBJECTS" % (self.origin))
        #                                                                      Pass in the station for gizmo_factory in the constructor
        listobjects = groundstation.transfer.request.Request("LISTALLOBJECTS", station=self.station)
        self.stream.enqueue(listobjects)
    else:
        log.info("object cache for %s still valid" % (self.origin))
    log.info("Handling LISTALLOBJECTS")
    payload = self.station.objects()
    if len(payload) > settings.LISTALLOBJECTS_CHUNK_THRESHOLD:
        log.info("Lots of objects to send, registering an iterator")

        @self.station.register_iter
        def iterator():
            for chunk in chunks(payload, settings.LISTALLOBJECTS_CHUNK_THRESHOLD):
                log.info("Sending %i object descriptions" % (len(chunk)))
                response = self._Response(self.id, "DESCRIBEOBJECTS",
                                        chr(0).join(chunk))
                self.stream.enqueue(response)
                yield
            self.TERMINATE()

    else:
        log.info("Sending %i object descriptions" % (len(payload)))
        response = self._Response(self.id, "DESCRIBEOBJECTS",
                                chr(0).join(payload))
        self.stream.enqueue(response)
        self.TERMINATE()
