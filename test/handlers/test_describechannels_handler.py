from support.handler_fixture import StationHandlerTestCase

from groundstation.proto.channel_list_pb2 import ChannelList

from groundstation.transfer.response_handlers import handle_describechannels
from groundstation.gref import Gref, Tip
from groundstation.objects.root_object import RootObject
from groundstation.objects.update_object import UpdateObject

import pygit2

from groundstation import logger
log = logger.getLogger(__name__)

import binascii

def _payload(obj, gref, tips):
    chunk = ChannelList()
    description = chunk.channels.add()
    description.channelname = gref.channel
    _gref = description.grefs.add()
    _gref.identifier = gref.identifier
    for tip in tips:
        _tip = _gref.tips.add()
        _tip.tip = tip
    return chunk.SerializeToString()


class TestHandlerDescribeChannels(StationHandlerTestCase):
    def test_handle_describechannels(self):
        test_id = u"tests/1"
        test_channel = u"test_channel"
        test_protocol = u"test_protocol"

        gref = Gref(self.station.station.store, test_channel, test_id)

        root_obj = RootObject(test_id, test_channel, test_protocol)
        root_oid = self.station.station.write(root_obj.as_object())
        current_oid = [root_oid]

        for i in xrange(10):
            update_obj = UpdateObject([current_oid.pop()], "loldata")
            current_oid.append(self.station.station.write(update_obj.as_object()))
        self.station.station.update_gref(gref, [Tip(root_oid, "")])
        self.assertEqual([root_oid], gref.tips())
        current_oid = current_oid.pop()

        self.station.payload = _payload(update_obj, gref, [current_oid])
        handle_describechannels(self.station)
        self.assertEqual([current_oid], gref.tips())

    # XXX Disabled for now, successully throws keyerrors when writing out invalid refs though
    def handle_describechannels_for_missing_tip(self):
        test_id = u"tests/1"
        test_channel = u"test_channel"
        test_protocol = u"test_protocol"

        gref = Gref(self.station.station.store, test_channel, test_id)

        root_obj = RootObject(test_id, test_channel, test_protocol)
        root_oid = self.station.station.write(root_obj.as_object())
        current_oid = [root_oid]

        for i in xrange(10):
            update_obj = UpdateObject([current_oid.pop()], "loldata")
            current_oid.append(self.station.station.write(update_obj.as_object()))

        update_obj = UpdateObject([current_oid.pop()], "loldata")
        current_oid.append(binascii.hexlify(pygit2.hash(update_obj.as_object())))

        self.station.station.update_gref(gref, [Tip(root_oid, "")])
        self.assertEqual([root_oid], gref.tips())
        current_oid = current_oid.pop()

        self.station.payload = _payload(update_obj, gref, [current_oid])
        handle_describechannels(self.station)
        self.assertEqual([current_oid], gref.tips())
