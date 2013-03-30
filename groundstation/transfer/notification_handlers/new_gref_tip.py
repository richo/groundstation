import groundstation.proto.channel_list_pb2
from groundstation.gref import Gref

from groundstation import logger
log = logger.getLogger(__name__)


def handle_newgreftip(self):
    proto_channels = groundstation.proto.channel_list_pb2.ChannelList()
    proto_channels.ParseFromString(self.payload)
    for channel in proto_channels.channels:
        for gref in channel.grefs:
            _gref = Gref(self.station.store, channel.channelname, gref.identifier)
            # Create a tip object to avoid upsetting fileutils
            tips = [tip.tip for tip in gref.tips]
            self.station.update_gref(_gref, tips, True)
