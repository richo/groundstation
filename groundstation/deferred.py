class Deferred(object):
    def __init__(self, at, thunk):
        self.at = at
        self.thunk = thunk

    def run(self):
        self.thunk()
