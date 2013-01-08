from groundstation import logger
log = logger.getLogger(__name__)


def handle_terminate(self):
    log.warn("Recieved unhandled event TERMINATE for request %s"
            % (str(self.id)))
