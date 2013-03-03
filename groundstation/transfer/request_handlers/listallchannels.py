import groundstation.proto.channel_list_pb2

from groundstation import logger
log = logger.getLogger(__name__)


def handle_listallchannels(self):
    log.info("Handling LISTALLCHANNELS")
    payload = self.station.channels()
    log.info("Sending %i channel descriptions" % (len(payload)))
    chunk = groundstation.proto.channel_list_pb2.ChannelList()
    for channel in payload:
        log.debug("serializing channel: %s" % (channel))
        description = chunk.channels.add()
        description.channelname = channel
        grefs = self.station.grefs(channel)
        for gref in grefs:
            log.debug("- serializing gref: %s" % (gref))
            _gref = description.grefs.add()
            _gref.identifier = gref.identifier
            for tip in gref:
                log.debug("-- serializing tip: %s" % (tip))
                _tip = _gref.tips.add()
                _tip.tip = tip
    response = self._Response(self.id, "DESCRIBECHANNELS",
            chunk.SerializeToString())
    self.stream.enqueue(response)
    self.TERMINATE()
