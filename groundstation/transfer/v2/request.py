class GeneratedResponse(object):
    """A response object that would be generated in response to a hydrated Request"""


class Request(object):
    """A Request object that can be serialized and enqueued to be sent"""
    def __init__(self, verb, station=None, stream=None, payload=None, origin=None):

