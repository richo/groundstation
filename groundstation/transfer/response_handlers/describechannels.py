import time
import groundstation.proto.channel_list_pb2

from groundstation import settings
from groundstation import logger
log = logger.getLogger(__name__)

from groundstation.gref import Gref

from groundstation.store import NoSuchObject


def handle_describechannels(self):
    if not self.payload:
        log.info("station %s sent empty DESCRIBECHANNELS payload - new database?" % (str(self.origin)))
        return

    retry_queued = False

    proto_channels = groundstation.proto.channel_list_pb2.ChannelList()
    proto_channels.ParseFromString(self.payload)
    for channel in proto_channels.channels:
        for gref in channel.grefs:
            _gref = Gref(self.station.store, channel.channelname, gref.identifier)
            # Create a tip object to avoid upsetting fileutils
            tips = [tip.tip for tip in gref.tips]
            try:
                self.station.update_gref(_gref, tips, True)
            except NoSuchObject:
                if not retry_queued:
                    retry_queued = True
                    log.warn("Objects missing, requeing fetch")
                    def thunk():
                        listchannels = groundstation.transfer.request.Request("LISTALLCHANNELS", station=self.station)
                        self.stream.enqueue(listchannels)
                    retry_at = time.time() + settings.LISTALLCHANNELS_RETRY_TIMEOUT
                    self.station.register_deferred(retry_at, thunk)
                else:
                    log.info("Retry already queued")
