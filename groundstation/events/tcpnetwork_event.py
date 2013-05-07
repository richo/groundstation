def payloads(sock):
    sock.recv()
    while sock.packet_queue:
        yield sock.packet_queue.pop()
