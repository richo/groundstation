# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: groundstation/proto/db_hash.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='groundstation/proto/db_hash.proto',
  package='',
  serialized_pb='\n!groundstation/proto/db_hash.proto\"&\n\x06\x44\x42Hash\x12\x0e\n\x06prefix\x18\x01 \x02(\t\x12\x0c\n\x04hash\x18\x02 \x01(\x0c')




_DBHASH = _descriptor.Descriptor(
  name='DBHash',
  full_name='DBHash',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='prefix', full_name='DBHash.prefix', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='hash', full_name='DBHash.hash', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=37,
  serialized_end=75,
)

DESCRIPTOR.message_types_by_name['DBHash'] = _DBHASH

class DBHash(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _DBHASH

  # @@protoc_insertion_point(class_scope:DBHash)


# @@protoc_insertion_point(module_scope)