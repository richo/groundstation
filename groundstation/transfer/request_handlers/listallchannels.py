import groundstation.proto.channel_list_pb2

from groundstation import logger
log = logger.getLogger(__name__)


def handle_listallchannels(self):
    log.info("Handling LISTALLCHANNELS")
    payload = self.station.channels()
    log.info("Sending %i object descriptions" % (len(payload)))
    chunk = groundstation.proto.channel_list_pb2.ChannelList()
    for channel in payload:
        description = chunk.channels.add()
        grefs = self.station.grefs(channel)
        for gref in grefs:
            _gref = description.grefs.add()
            _gref.name = gref.identifier
            for tip in gref:
                _tip = _gref.tips.add()
                _tip.tip = tip
    response = self._Response(self.id, "DESCRIBECHANNELS",
            chunk.SerializeToString())
    self.stream.enqueue(response)
    self.TERMINATE()
