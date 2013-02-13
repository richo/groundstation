proto: groundstation/proto/gizmo_pb2.py groundstation/proto/git_object_pb2.py groundstation/proto/object_list_pb2.py groundstation/objects/root_object_pb2.py groundstation/objects/update_object_pb2.py

PROTOC_OPTS = --python_out=./

groundstation/proto/gizmo_pb2.py: groundstation/proto/gizmo.proto
	protoc ${PROTOC_OPTS} groundstation/proto/gizmo.proto

groundstation/proto/git_object_pb2.py: groundstation/proto/git_object.proto
	protoc ${PROTOC_OPTS} groundstation/proto/git_object.proto

groundstation/proto/object_list_pb2.py: groundstation/proto/object_list.proto
	protoc ${PROTOC_OPTS} groundstation/proto/object_list.proto

groundstation/objects/root_object_pb2.py: groundstation/objects/root_object.proto
	protoc ${PROTOC_OPTS} groundstation/objects/root_object.proto

groundstation/objects/update_object_pb2.py: groundstation/objects/update_object.proto
	protoc ${PROTOC_OPTS} groundstation/objects/update_object.proto

clean:
	find ./ -iname "*.pyc" -delete

_test:

test: _test
	GROUNDSTATION_DEBUG=WARN python -m unittest discover test
