import logger
log = logger.getLogger(__name__)

class RequestRegistry(object):
    def __init__(self):
        self._reg = {}

    @property
    def contents(self):
        return self._reg

    def __contains__(self, other):
        return str(other) in self._reg

    def register(self, req):
        if req.id in self:
            log.warn("%s already registered in %s" % (repr(req), repr(self)))
        self._reg[str(req.id)] = req

    def free(self, req):
        if req.id not in self:
            log.warn("%s (id: %s) not registered in %s" % (repr(req), repr(req.id), repr(self)))
            return False
        else:
            return self._reg.pop(str(req.id))

    def __getitem__(self, key):
        return self._reg[str(key)]
