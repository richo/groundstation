import groundstation.transfer.request

from groundstation import logger
log = logger.getLogger(__name__)

def handle_fetchobject(self):
    log.info("Handling FETCHOBJECT for %s" % (repr(self.payload)))
    response = self._Response(self.id, "TRANSFER", self.station.repo[self.payload])
    self.stream.enqueue(response)
