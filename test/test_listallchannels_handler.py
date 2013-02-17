from handler_fixture import StationHandlerTestCast

from groundstation.transfer.request_handlers import handle_listallchannels
from groundstation.gref import Gref
from groundstation.objects.root_object import RootObject



class TestHandlerListAllChannels(StationHandlerTestCast):
    def test_handle_listallchannels(self):
        test_id = "tests/1"
        test_channel = "test_channel"
        test_protocol = "test_protocol"

        obj = RootObject(test_id, test_channel, test_protocol)
        gref = Gref(self.station.station.store, test_channel, test_id)

        oid = self.station.station.write(obj.as_object())
        self.station.station.update_gref(gref, [oid], [])

        handle_listallchannels(self.station)
        response = self.station.stream.pop()
        assert len(self.station.stream) == 0, "Someone is leaving objects lyind around"
        print response.payload
