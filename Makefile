proto: groundstation/proto/gizmo_pb2.py

groundstation/proto/gizmo_pb2.py:
	protoc --python_out=./ groundstation/proto/gizmo.proto
