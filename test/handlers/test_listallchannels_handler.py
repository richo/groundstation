from support.handler_fixture import StationHandlerTestCase

from groundstation.transfer.request_handlers import handle_listallchannels
from groundstation.gref import Gref, Tip
from groundstation.objects.root_object import RootObject
from groundstation.proto.channel_list_pb2 import ChannelList


class TestHandlerListAllChannels(StationHandlerTestCase):
    def test_handle_listallchannels(self):
        test_id = u"tests/1"
        test_channel = u"test_channel"
        test_protocol = u"test_protocol"

        obj = RootObject(test_id, test_channel, test_protocol)
        gref = Gref(self.station.station.store, test_channel, test_id)

        oid = self.station.station.write(obj.as_object())
        self.station.station.update_gref(gref, [Tip(oid, "")], [])

        handle_listallchannels(self.station)
        response = self.station.stream.pop()
        serialized_response = response.SerializeToString()
        self.assertIsInstance(serialized_response, str)
        assert len(self.station.stream) == 0, "Someone is leaving objects lyind around"
        channel_description = ChannelList()
        channel_description.ParseFromString(response.payload)
        self.assertEqual(channel_description.channels[0].channelname, test_channel)
        self.assertEqual(channel_description.channels[0].grefs[0].identifier, test_id)
        self.assertEqual(channel_description.channels[0].grefs[0].tips[0].tip, oid)
