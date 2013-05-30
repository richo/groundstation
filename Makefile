all: proto

.PHONY: proto test

proto: groundstation/proto/gizmo_pb2.py \
	groundstation/proto/git_object_pb2.py \
	groundstation/proto/object_list_pb2.py \
	groundstation/proto/channel_list_pb2.py \
	groundstation/proto/db_hash_pb2.py \
	groundstation/objects/base_object_pb2.py \
	groundstation/objects/root_object_pb2.py \
	groundstation/objects/update_object_pb2.py

PROTOC_OPTS = --python_out=./

groundstation/%_pb2.py: groundstation/%.proto
	protoc ${PROTOC_OPTS} $^

clean:
	find ./ -iname "*.pyc" -delete

groundstation_test:
	GROUNDSTATION_DEBUG=WARN python -m unittest discover test

airship_test:
	cd airship; ../node_modules/mocha/bin/mocha

test: groundstation_test airship_test
