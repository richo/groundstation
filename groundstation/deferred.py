class Deferred(object):
    def __init__(self, at, thunk):
        self.at = at
        self.thunk = thunk

    def run(self):
        self.thunk()


def defer_until(at):
    def make_deferred(thunk):
        return Deferred(at, thunk)
    return make_deferred
