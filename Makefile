proto: groundstation/proto/gizmo_pb2.py groundstation/proto/git_object_pb2.py

groundstation/proto/gizmo_pb2.py: groundstation/proto/gizmo.proto
	protoc --python_out=./ groundstation/proto/gizmo.proto

groundstation/proto/git_object_pb2.py: groundstation/proto/git_object.proto
	protoc --python_out=./ groundstation/proto/git_object.proto

clean:
	find ./ -iname "*.pyc" -delete

_test:

test: _test
	GROUNDSTATION_DEBUG=WARN python -m unittest discover test
