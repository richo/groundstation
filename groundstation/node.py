import uuid

from groundstation import logger
log = logger.getLogger(__name__)

class Node(object):
    def __init__(self):
        self.uuid = uuid.uuid1()
        self.name = str(self.uuid)
        log.info("Node started with id %s" % self.name)
