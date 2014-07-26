import struct
import base64

import quietnet.listen as listen
from groundstation.gref import Gref, Tip

from groundstation import logger
log = logger.getLogger(__name__)

def reset_header():
    return 0, [0, 0], None

def reset_payload():
    return list()

class AudioReceiver(object):
    def __init__(self, freq, station):
        self.freq = freq
        self.station = station

    def start_listening(self):
        header_byte_count, header_bytes, header_length = reset_header()
        payload = reset_payload()
        listen.setup_processes()
        for char in listen.start_analysing_stream():
            char_value = ord(char)
            if char_value & 0b10000000: # Header byte
                log.info("Header byte: %s" % (bin(char_value)))
                if header_byte_count == 0: # First header byte
                    header_bytes[0] |= char_value & 0xf
                    header_byte_count += 1
                elif header_byte_count == 1:
                    header_bytes[0] |= (char_value & 0xf) << 4
                    header_byte_count += 1
                elif header_byte_count == 2:
                    header_bytes[1] |= (char_value & 0xf)
                    header_byte_count += 1
                elif header_byte_count == 3:
                    header_bytes[1] |= (char_value & 0xf) << 4
                    header_byte_count += 1
                    header_length = struct.unpack(">h", ''.join(map(chr, header_bytes)))[0]
                    log.info("Reading %d bytes of payload" % header_length)
                elif header_byte_count == 4:
                    log.warning("Got header bytes while still expecting payload")
                    payload.append(char)

            else: # Payload byte
                if header_length == 0:
                    log.warning("Got payload bytes when expecting header")
                payload.append(char)
                if len(payload) % 8 == 0:
                    log.info("Got %d bytes so far" % (len(payload)))
                if len(payload) == header_length:
                    log.info("Got all of object")
                    decoded = base64.b64decode(''.join(payload))
                    log.info("Writing payload to DB")
                    oid = self.station.write(decoded)
                    log.info("Wrote object, got: %s" % (repr(oid)))
                    Gref(self.station.store, "soundstation", "demo")
                    try:
                        self.station.update_gref(g, [Tip(oid, "")], []) # yolo
                    except:
                        pass

                    header_byte_count, header_bytes, header_length = reset_header()
                    payload = reset_payload()
