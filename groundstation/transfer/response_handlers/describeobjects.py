from groundstation import logger
log = logger.getLogger(__name__)


def handle_describeobjects(self):
    if not self.payload:
        log.info("station %s sent empty DESCRIVEOBJECTS payload - new database?" % (str(self.origin)))
        return
    for obj in self.payload.split(chr(0)):
        if obj not in self.station:
            request = self._Request("FETCHOBJECT", payload=obj)
            self.stream.enqueue(request)
        else:
            log.debug("Not fetching already present object %s" % (str(obj)))
