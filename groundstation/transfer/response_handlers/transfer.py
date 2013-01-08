from groundstation import logger
log = logger.getLogger(__name__)


def handle_transfer(self):
    log.info("Handling TRANSFER of %s" % (self.payload))
    ret = self.station.write_object(self.payload)
    log.info("Wrote object %s" % (repr(ret)))
