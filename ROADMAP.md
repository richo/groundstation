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
