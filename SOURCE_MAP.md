Groundstation Source Map
========================

stationd
--------

stationd runs a station on the local network. By default it:

- Runs a BroadcastListener which detects peers on the local
- Runs a BroadcastAnnouncer which announces its presence to available listeners
- maintains a SocketPool of peers which were discovered using the Broadcast* handlers.

airshipd
--------

airshipd runs the backend for the javascript frontend. By default it:

- Binds a webserver on port 9005
- Serves up everything needed to visualise and interact with your groundstation db

script/cibuild
--------------

runs the tests, as well as some generic setup tasks. Intended to be run in a CI server.

script/dump_gref
----------------

given a channel and a gref, dumps a `git log --graph` like structure to the terminal.

Currently buggy for complex relationships.

script/slurp_github
-------------------

given a valid github token in `GITHUB_TOKEN` environment variable, pulls the
issue structure from either a single repo, (`--repo richo/groundstation`) or
all public repos the key has push access to (`--all`)

script/slurp_jira
-----------------

Similar in design to slurp github, but targeted at JIRA
