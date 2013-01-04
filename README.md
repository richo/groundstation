groundstation
=============

groundstation is a decentralised task/project management suite.

The core of it's implementation is an object store of linked immutable objects
that are synced via a gossip protocol.

The current version uses libgit2 as a storage backend, but doesn't use many git
primitives, beyond git's objects as a storage medium. This may change in the
future.

pygit2
------

groundstation uses pygit2 under the hood for it's git interactions, and some
features that it depends on have not landed in a stable release yet.

For this reason, you'll need to build and install the latest [libgit2](1) and
[pygit2](2) from source.

[1]:http://libgit2.github.com/
[2]:https://github.com/libgit2/pygit2#building-on-nix-including-os-x
