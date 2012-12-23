groundstation
=============

groundstation is a decentralised task/project management suite.

The core of it's implementation is an object store of linked immutable objects
that are synced via a gossip protocol.

The current version uses libgit2 as a storage backend, but doesn't use many git
primitives, beyond git's objects as a storage medium. This may change in the
future.
