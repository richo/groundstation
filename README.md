groundstation
=============

groundstation is a database, and framework for operating with the database,
intended to build distributed knowledge graphs, and then sync them up in
hostile network settings.

The core of its implementation is an object store of linked immutable objects
that are synced via a gossip protocol.

The current version uses libgit2 as a storage backend, but doesn't use many git
primitives, beyond git's objects as a storage medium. Git is deliberately
pulled out into a storage driver, however while groundstation doesn't assume
that you're using git it does assume you're using something that looks *a lot
like git*.

protocol support
----------------

groundstation hinges on the notion of protocols internally – groundstation core
provides you with content addressable storage, but it's up to you to work out
what to actually do with that data.

That said, groundstation does ship with some protocol adaptors. Adaptors take
the form `name@domain:adaptor-version`, and until such time as a release is
already, everything that ships with groundstation will be released with
`richo@psych0tik.net` as the email, ie `richo@psych0tik.net:github-0.0.0`.


development
-----------

groundstation is mostly self contained, and hasn't relied on unreleased
features in libgit2 or pygit2 for some time now. Assuming that you have a
working and recent libgit2 you should be able to run the test suite by running:

Groundstation should work with the latest stable version of pygit2, which
unfortunately still depends on an unreleased version of libgit2. It has been a
while since I used new features in pygit2 though, so older versions should work
fine as far back as 0.18.


1. install libgit2 from the `development` branch.
2. `pip install -r requirements.txt` (On OSX you'll need to `export CC=clang` for pycrypto)
3. `make groundstation_dev`

You probably want to install those requirements in a virtualenv.

There is also a tiny unittest suite for some of the javascript in Airship, you can run them by running:

1. `npm install`
2. `make airship_test`

You'll almost certainly want to have a read of the [hacking document](HACKING.md),
and check out the other [misc hacking docs](HACKING/).
