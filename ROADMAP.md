roadmap
=======

Or, all the stuff I'd like to have at some point:

### Sync drivers

Sync is currently driven by the One True Strategy. The sync API should be much
smarter, and easier to hack on.

* Work is in progress with StreamClient#begin_handshake. This should be expanded.
* Sync Drivers should be implemented for:
 - Fetch All Objects
 - Fetch All Grefs (And all dependent objects)
 - Fetch All Signed Grefs (And all dependent objects)
 - Fetch All Objects from an authenticated party, with fallback

### Integration Testing

Integration testing is currently super awkward. Building an internal framework
for sanely mapping out integration tests needs doing soonish

### Garbage Collection

By creating trees of relevant objects, and then pointing at them with junk
refs, it should be possible to get the db into a state where `git gc --prune`
will actually remove objects that are no longer needed.

This in turn needs to be orchestrated with a cache to make sure they're not
collected again, and in turn (again) potentially with Station#get_hash to
ensure that we're equivalent as someone who hasn't removed them.

### Configurable sync depth

Retrieving some order of magnitude of the objects a station is intending to
fetch would help the sync driver choose and appropriate depth for the db_hash
sync strategy
