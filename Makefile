proto: groundstation/proto/gizmo_pb2.py groundstation/proto/request_pb2.py groundstation/proto/response_pb2.py

groundstation/proto/gizmo_pb2.py: groundstation/proto/gizmo.proto
	protoc --python_out=./ groundstation/proto/gizmo.proto

groundstation/proto/request_pb2.py: groundstation/proto/request.proto
	protoc --python_out=./ groundstation/proto/request.proto

groundstation/proto/response_pb2.py: groundstation/proto/response.proto
	protoc --python_out=./ groundstation/proto/response.proto

clean:
	find ./ -iname "*.pyc" -delete

_test:

test: _test
	python -m unittest discover test
