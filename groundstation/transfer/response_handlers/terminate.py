from groundstation import logger
log = logger.getLogger(__name__)


def handle_terminate(self):
    if self.station.free_request(self):
        log.info("Freed request %s" % (str(self.id)))
    else:
        log.info("Failed to free request %s" % (str(self.id)))
