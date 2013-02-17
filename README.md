groundstation
=============

groundstation is a decentralised task/project management suite.

The core of its implementation is an object store of linked immutable objects
that are synced via a gossip protocol.

The current version uses libgit2 as a storage backend, but doesn't use many git
primitives, beyond git's objects as a storage medium. This may change in the
future.

pygit2
------

groundstation uses pygit2 under the hood for its git interactions, and some
features that it depends on have not landed in a stable release yet.

For this reason, you'll need to build and install the latest [libgit2](1) and
[pygit2](2) from source.

protocol support
----------------

groundstation hinges on the notion of protocols internally- groundstation core
provides you with content addressable storage, but it's up to you to work out
what to actually do with that data.

That said, groundstation does ship with some protocol adaptors. Adaptors take
the form `name@domain:adaptor-version`, and until such time as a release is
already, everything that ships with groundstation will be released with
`richo@psych0tik.net` as the email.


development
-----------

1. install development libgit2 (on OSX this is streamlined by `brew install --HEAD libgit2`)
2. `pip install -r requirements.txt`
3. ???????
4. profit!

[1]:http://libgit2.github.com/
[2]:https://github.com/libgit2/pygit2#building-on-nix-including-os-x
