# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: DataEntry.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='DataEntry.proto',
  package='sharepubapi_v1',
  syntax='proto3',
  serialized_options=_b('\n$com.yoti.api.client.spi.remote.protoB\016DataEntryProtoZ\016yotiprotoshare\252\002\030Yoti.Auth.ProtoBuf.Share\312\002\020Yoti\\Sharepubapi\342\002\034Yoti\\Sharepubapi\\GPBMetadata\352\002\031Yoti.Protobuf.Sharepubapi'),
  serialized_pb=_b('\n\x0f\x44\x61taEntry.proto\x12\x0esharepubapi_v1\"\xdd\x01\n\tDataEntry\x12,\n\x04type\x18\x01 \x01(\x0e\x32\x1e.sharepubapi_v1.DataEntry.Type\x12\r\n\x05value\x18\x02 \x01(\x0c\"\x92\x01\n\x04Type\x12\r\n\tUNDEFINED\x10\x00\x12\x0b\n\x07INVOICE\x10\x01\x12\x17\n\x13PAYMENT_TRANSACTION\x10\x02\x12\x0c\n\x08LOCATION\x10\x03\x12\x0f\n\x0bTRANSACTION\x10\x04\x12\x1b\n\x17\x41GE_VERIFICATION_SECRET\x10\x05\x12\x19\n\x15THIRD_PARTY_ATTRIBUTE\x10\x06\x42\xaf\x01\n$com.yoti.api.client.spi.remote.protoB\x0e\x44\x61taEntryProtoZ\x0eyotiprotoshare\xaa\x02\x18Yoti.Auth.ProtoBuf.Share\xca\x02\x10Yoti\\Sharepubapi\xe2\x02\x1cYoti\\Sharepubapi\\GPBMetadata\xea\x02\x19Yoti.Protobuf.Sharepubapib\x06proto3')
)



_DATAENTRY_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='sharepubapi_v1.DataEntry.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNDEFINED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVOICE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PAYMENT_TRANSACTION', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOCATION', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TRANSACTION', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AGE_VERIFICATION_SECRET', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='THIRD_PARTY_ATTRIBUTE', index=6, number=6,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=111,
  serialized_end=257,
)
_sym_db.RegisterEnumDescriptor(_DATAENTRY_TYPE)


_DATAENTRY = _descriptor.Descriptor(
  name='DataEntry',
  full_name='sharepubapi_v1.DataEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='sharepubapi_v1.DataEntry.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='sharepubapi_v1.DataEntry.value', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DATAENTRY_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=36,
  serialized_end=257,
)

_DATAENTRY.fields_by_name['type'].enum_type = _DATAENTRY_TYPE
_DATAENTRY_TYPE.containing_type = _DATAENTRY
DESCRIPTOR.message_types_by_name['DataEntry'] = _DATAENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DataEntry = _reflection.GeneratedProtocolMessageType('DataEntry', (_message.Message,), dict(
  DESCRIPTOR = _DATAENTRY,
  __module__ = 'DataEntry_pb2'
  # @@protoc_insertion_point(class_scope:sharepubapi_v1.DataEntry)
  ))
_sym_db.RegisterMessage(DataEntry)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
