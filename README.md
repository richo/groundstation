groundstation
=============

groundstation is a database, and framework for operating with the database,
intended to build distributed knowledge graphs, and then sync them up in
hostile network settings.

It's uses are wide and varied, but some key examples are:

* Locale driven marketplaces.
* Fully decentralised bulletin boards.
* Networks that keep working long after the internet has failed.

The core of its implementation is an object store of linked immutable objects
that are synced via a gossip protocol.

The current version uses libgit2 as a storage backend, but doesn't use many git
primitives, beyond git's objects as a storage medium. Git is deliberately
pulled out into a storage driver, however while groundstation doesn't assume
that you're using git it does assume you're using something that looks *a lot
like git*.

pygit2
------

groundstation uses pygit2 under the hood for its git interactions, and some
features that it depends on have not landed in a stable release yet.

For this reason, you'll need to build and install the latest [libgit2][1] from
source.

protocol support
----------------

groundstation hinges on the notion of protocols internally- groundstation core
provides you with content addressable storage, but it's up to you to work out
what to actually do with that data.

That said, groundstation does ship with some protocol adaptors. Adaptors take
the form `name@domain:adaptor-version`, and until such time as a release is
already, everything that ships with groundstation will be released with
`richo@psych0tik.net` as the email, ie `richo@psych0tik.net:github-0.0.0`.


development
-----------

groundstation uses [babashka][3] for managing its dependencies. If you have it installed, you should be able to do something like:

`babashka groundstation_dev` and wind up with a working environment. Maybe.

1. install libgit2 v0.18.0
2. `pip install -r requirements.txt`
3. ???????
4. profit!

You probably want to install those requirements in a virtualenv.

You'll almost certainly want to have a read of the [hacking document](HACKING.md),
and checkout the other [misc hacking docs](HACKING/).

[1]:http://libgit2.github.com/
[2]:https://github.com/libgit2/pygit2#building-on-nix-including-os-x
[3]:https://github.com/richo/babashka
