# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ExtraData.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import DataEntry_pb2 as DataEntry__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ExtraData.proto',
  package='sharepubapi_v1',
  syntax='proto3',
  serialized_options=_b('\n$com.yoti.api.client.spi.remote.protoB\016ExtraDataProtoZ\016yotiprotoshare\252\002\030Yoti.Auth.ProtoBuf.Share\312\002\020Yoti\\Sharepubapi\342\002\034Yoti\\Sharepubapi\\GPBMetadata\352\002\031Yoti.Protobuf.Sharepubapi'),
  serialized_pb=_b('\n\x0f\x45xtraData.proto\x12\x0esharepubapi_v1\x1a\x0f\x44\x61taEntry.proto\"4\n\tExtraData\x12\'\n\x04list\x18\x01 \x03(\x0b\x32\x19.sharepubapi_v1.DataEntryB\xaf\x01\n$com.yoti.api.client.spi.remote.protoB\x0e\x45xtraDataProtoZ\x0eyotiprotoshare\xaa\x02\x18Yoti.Auth.ProtoBuf.Share\xca\x02\x10Yoti\\Sharepubapi\xe2\x02\x1cYoti\\Sharepubapi\\GPBMetadata\xea\x02\x19Yoti.Protobuf.Sharepubapib\x06proto3')
  ,
  dependencies=[DataEntry__pb2.DESCRIPTOR,])




_EXTRADATA = _descriptor.Descriptor(
  name='ExtraData',
  full_name='sharepubapi_v1.ExtraData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='list', full_name='sharepubapi_v1.ExtraData.list', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=52,
  serialized_end=104,
)

_EXTRADATA.fields_by_name['list'].message_type = DataEntry__pb2._DATAENTRY
DESCRIPTOR.message_types_by_name['ExtraData'] = _EXTRADATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ExtraData = _reflection.GeneratedProtocolMessageType('ExtraData', (_message.Message,), dict(
  DESCRIPTOR = _EXTRADATA,
  __module__ = 'ExtraData_pb2'
  # @@protoc_insertion_point(class_scope:sharepubapi_v1.ExtraData)
  ))
_sym_db.RegisterMessage(ExtraData)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
