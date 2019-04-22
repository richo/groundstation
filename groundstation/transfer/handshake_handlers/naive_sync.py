from groundstation.transfer.request import Request

class NaiveHandshakeHandler(object):
    def __init__(self, station):
        self.station = station

    def begin_handshake(self, station):
        request = Request("LISTALLOBJECTS", station=station, stream=self)
        self.station.register_request(request)
        station.enqueue(request)
