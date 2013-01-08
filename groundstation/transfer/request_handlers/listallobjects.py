import groundstation.transfer.request

from groundstation import logger
log = logger.getLogger(__name__)

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
    log.info("Sending %i object descriptions" % (len(payload)))
    response = self._Response(self.id, "DESCRIBEOBJECTS",
                            chr(0).join(payload))
    self.stream.enqueue(response)
    self.TERMINATE()
