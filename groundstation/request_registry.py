import logger
log = logger.getLogger(__name__)

class RequestRegistry(object):
    def __init__(self):
        self._reg = {}

    def __contains__(self, other):
        return str(other) in self._reg

    def register(self, req):
        if req.requestid in self:
            log.warn("%s already registered in %s" % (repr(req), repr(self)))
        self._reg[str(req.requestid)] = req

    def free(self, req):
        if req.requestid not in self:
            log.warn("%s (id: %s) not registered in %s" % (repr(req), repr(req.requestid), repr(self)))
        else:
            del self._reg[str(req.requestid)]

    def __getitem__(self, key):
        return self._reg[str(key)]
