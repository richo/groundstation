PROTOC_OPTS = --python_out=./
proto: groundstation/proto/gizmo_pb2.py groundstation/proto/response/transfer_pb2.py

groundstation/proto/gizmo_pb2.py: groundstation/proto/gizmo.proto
	protoc ${PROTOC_OPTS} groundstation/proto/gizmo.proto

groundstation/proto/response/transfer_pb2.py: groundstation/proto/response/transfer.proto
	protoc ${PROTOC_OPTS} groundstation/proto/response/transfer.proto

clean:
	find ./ -iname "*.pyc" -delete

_test:

test: _test
	python -m unittest discover test
