Protocol Specification for groundstation
========================================

## Discovery

* Nodes will bind to a UDP socket, and a TCP port on $PORT.
* Nodes will periodically broadcast to any peers listening on UDP.
* A node recieving a UDP broadcast will first check it's existing received
    connection pool, before immediately connecting to the broadcasting party to
    arrange an exchange of data.

## Database

* Currently uses git object database.
* stationd will be single threaded by design to avoid bizarre syncronisation
  issues; and also because microsleeps in the network code will not be
  userfacing.
* The db is atomic and concurrent, any number of clients may read and write
  objects concurrently.
* stationd shall implement a notification type to allow clients (web ui, native
  etc) to be notified immediately of new data.

## Transfer of data

* Data transfer takes place by sending packs `msg length``NUL``protobuf` to peers.
* msg length is sent ascii encoded for ease or porting and debugging.

#### Requests take the form
```javascript
{
    "type": REQUEST,
    "verb": KEYWORD,    // KEYWORDs include LISTALLOBJECTS FETCHOBJECT
    "id": UUID,         // UUID shall be a uuid to marry up with the response
    "payload": PAYLOAD or NULL
}
```

#### Responses take the form
```javascript
{
    "type": RESPONSE,
    "verb": KEYWORD, // KEYWORDs include TRANSFER and TERMINATE. more than a
                       // single response is valid for a request, TERMINATE
                       // signifies that the storage allocated to the request
                       // may be freed
    "id": UUID,        // The UUID sent with the request. In the case
    "payload": PAYLOAD or NULL
}
```

* When a node is discovered by Broadcast, the UUID's are compared and the lower
  ID will connect to the higher.
* When a connection is initialized, the recieving node will check if it already
  has a connection to the given party and sever it in that case.
* Should the connection not be severed, the connecting party shall immediately
  issue a `LISTALLOBJECTS` request. This will essentially kick off the event
  loop, at this point all requests can be responded to in kind as a result of
  the ordinary event loop without outside interference.

### Request Types

Currently supported are

#### LISTALLOBJECTS

Doesn't accept a payload. Response should be a single `DESCRIBEOBJECT` with a
null seperated list of object ID's as the payload

#### FETCHOBJECT

Accepts a payload of the object id to fetch. Returns a `TRANSFER` with a blob
body (content) as the payload.

### Response Types

#### DESCRIBEOBJECT

Accepts a list of object ID's null seperated. Usually yields some
`FETCHOBJECT`s for any missing objects in the local db.

#### TRANSFER

Accepts an object body as a payload, to be inserted into a target database

#### TERMINATE

Specifies that a given `REQUEST` is fulfilled and may be freed.
