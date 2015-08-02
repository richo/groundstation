#!/usr/bin/env python
def log(msg):
    print("[+] %s" % msg)

import os
import sys

import bz2

from groundstation.station import Station
from groundstation.node import Node

from groundstation.objects.update_object import UpdateObject

def main():
    myself = Node()
    station = Station.from_env(myself)

    for obj in station.objects():
        data = station[obj]
        o = UpdateObject.from_object(data.read_raw())
        filename, body = o.data.split(chr(0x00), 1)
        log("%s: %s" % (obj, filename))
        print(bz2.decompress(body))


if __name__ == '__main__':
    main()


