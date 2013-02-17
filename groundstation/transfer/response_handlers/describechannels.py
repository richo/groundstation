import groundstation.proto.channel_list_pb2

from groundstation import logger
log = logger.getLogger(__name__)

from groundstation.gref import Gref


def handle_describechannels(self):
    if not self.payload:
        log.info("station %s sent empty DESCRIBECHANNELS payload - new database?" % (str(self.origin)))
        return
    proto_channels = groundstation.proto.channel_list_pb2.ChannelList()
    proto_channels.ParseFromString(self.payload)
    for channel in proto_channels.channels:
        for gref in channel.grefs:
            _gref = Gref(self.station.store, channel.channelname, gref.identifier)
            self.station.update_gref(_gref, _gref.tips())




