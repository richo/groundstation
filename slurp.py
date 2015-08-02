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
    filename = sys.argv[1]
    log("Stealing %s" % filename)

    with open(filename) as fh:
        obj = UpdateObject([],
            os.path.basename(filename) +
            chr(0x00) +
            bz2.compress(fh.read())
            )
        name = station.write(obj.as_object())
        log("Wrote %s into stationdb" % name)



if __name__ == '__main__':
    main()
