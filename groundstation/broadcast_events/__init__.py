from broadcast_ping import BroadcastPing

EVENT_TYPES = {
        "PING": BroadcastPing,
}

class UnknownBroadcastEvent(Exception):
    pass

def new_broadcast_event(data):
    event_type, payload = data.split(" ", 1)
    if event_type not in EVENT_TYPES:
        raise UnknownBroadcastEvent(event_type)
    return EVENT_TYPES[event_type](payload)
