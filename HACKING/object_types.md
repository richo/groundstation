RootObject
==========

NB: See [protocol](/groundstation/objects/root_object.proto) and [implementation](/groundstation/objects/root_object.py)

This is the root object of a thread. It contains:
- SHA1: This is the hash of the object as stored in the objdb, as used for checksumming.
- ID: This should be reproducable if it's from upstream
    - github:richo/groundstation/issues/15 for example
    - They will be identifiable by the sha1 of the id
- Channel: This is a unique id for an object's parent, ie:
    - email:richo@psych0tik.net:TODO
    - github:richo/groundstation
    - bitbucket:larsyencken/doko
- Protocol: This is the internal codec for objectUpdate data, it shoudl include an as yet unspecified version.
    - richo@psych0tik.net:TODO
    - richo@psych0tik.net:github:issues

ObjectUpdate
============

NB: See [protocol](/groundstation/objects/update_object.proto) and [implementation](/groundstation/objects/update_object.py)

These represent the updates to an object. The format of the payload member is dependent on the value of Protocol on the root object, but should include:

- parent: This shall be an array of ID's of parents. Note that this is the SHA hashes and not the stringified ID.
- data: An a protocol (as specified on the rootObject) specific payload used by the adaptor to render the content.
