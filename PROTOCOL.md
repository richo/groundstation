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

