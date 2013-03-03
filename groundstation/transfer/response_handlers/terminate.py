from groundstation import logger
log = logger.getLogger(__name__)


def handle_terminate(self):
    req = self.station.free_request(self)
    if req:
        log.info("Freed request %s" % (str(self.id)))
        req.teardown()
    else:
        log.info("Failed to free request %s" % (str(self.id)))
