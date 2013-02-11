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

object trees
------------

For obvious reasons, objects can't contain forward references without changing
their hashes and thereby making themselves useless. This makes walking the tree
forwards difficult, especially as it makes writing out indexes in any
meaningful way impossible without enforcing cross repository locking. My
current tentative solution to this is as follows:

### Indexing

Given an object `a`, with forward ancestors `b`, `c`, and `d` such that the
tree looks like:

```
a--b--c
     \
      d
```

1. An indexing process will start at one of the foremost nodes (at time of
writing, this should occur when new objects are written with ancestors)

2. This process should enumerate it's ancestors, writing them out to a tempfile
in the repository (tentatively in `/tmp/$$/...` for dotlocking) one hash per
line, in reverse order, ie most recent commit first.

3. Upon completion, this process will use an atomic `mv`/`rename`
implementation to create a file in `$objdb/rindex` with the name of the object
whose history has been enumerated.

4. This process may at it's option then unlink the files named by any ancestors
named in the file just written.

### Traversing

To find the forward ancestors of a given object, simply grep over
`$odjdb/reindex` for the commit has in question. the filenames represent the
tips, any intermediate nodes are contained inside the file.
