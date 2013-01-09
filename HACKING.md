Development
===========

Developing for groundstation is made awkward by it's design. I'm finding that
Vagrant works reasonably well, a Vagrantfile is distributed in HACKING/

Stations
========

The station is the core of groundstation. It represents a warpper around (For
now) a single git object database. the network stuff isn't directly related,
but the sole purpose of groundstations network stack is to interact with a
station object.

stationd
========

Stationd implements an event driven mainloop. This loop blocks on the sockets
(streaming and discovery), but allows allows events to be bound up for the
"next tick" in the form of iterators.

Because iterators will tend to queue up some outgoing network IO, for this
reason you won't be at the mercy of the event loop while waiting for IO to
happen, but should your sockets start blocking, you won't be allowed to write,
although even then your packets are written to a queue and not directly to the
socket, so this shouldn't be something you need to be concerned about.
