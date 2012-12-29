proto: groundstation/proto/gizmo_pb2.py

groundstation/proto/gizmo_pb2.py: groundstation/proto/gizmo.proto
	protoc --python_out=./ groundstation/proto/gizmo.proto

clean:
	find ./ -iname "*.pyc" -delete
