from groundstation import logger
log = logger.getLogger(__name__)

def handle_listallobjects(self):
    if not self.station.recently_queried(self.origin):
        log.info("%s not up to date, issuing LISTALLOBJECTS" % (self.origin))
        listobjects = Request("LISTALLOBJECTS")
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
