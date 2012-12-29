* Rip out the ad hoc payload transfer stuff, use protocol buffers
* Boilerplate to allow enqueue()'ing an iterator to avoid being a noisy neighbour.
* Rework the request/reply cycle and the mechanism to pass a Station into the request/response factories
* Unify on FooException or FooError
* LISTALLOBJECTS actually sends the objects in the response, instead of a list..
* Work out the station semantics for gizmo_factory. Not having globals is all well and good but this is getting retarded.
* Manage a state table for all requests (honouring TERMINATE) and end connections when all requests are fulfilled.
