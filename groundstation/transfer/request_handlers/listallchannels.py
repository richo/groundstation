import groundstation.proto.channel_list_pb2

from groundstation import logger
log = logger.getLogger(__name__)


def handle_listallchannels(self):
    log.info("Handling LISTALLCHANNELS")
    payload = self.station.channels()
    log.info("Sending %i object descriptions" % (len(payload)))
    chunk = groundstation.proto.channel_list_pb2.ChannelList()
    for obj in payload:
        chunk.channelname.append(payload)
    response = self._Response(self.id, "DESCRIBECHANNELS",
            chunk.SerializeToString())
    self.stream.enqueue(response)
    self.TERMINATE()
