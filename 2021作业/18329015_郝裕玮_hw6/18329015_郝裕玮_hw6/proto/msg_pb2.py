# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: msg.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='msg.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\tmsg.proto\"\x1a\n\nMsgRequest\x12\x0c\n\x04text\x18\x01 \x01(\t\")\n\x0bMsgResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0e\n\x06result\x18\x02 \x01(\t23\n\nMsgService\x12%\n\x06GetMsg\x12\x0b.MsgRequest\x1a\x0c.MsgResponse\"\x00\x62\x06proto3'
)




_MSGREQUEST = _descriptor.Descriptor(
  name='MsgRequest',
  full_name='MsgRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='MsgRequest.text', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=13,
  serialized_end=39,
)


_MSGRESPONSE = _descriptor.Descriptor(
  name='MsgResponse',
  full_name='MsgResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='MsgResponse.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='result', full_name='MsgResponse.result', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=41,
  serialized_end=82,
)

DESCRIPTOR.message_types_by_name['MsgRequest'] = _MSGREQUEST
DESCRIPTOR.message_types_by_name['MsgResponse'] = _MSGRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MsgRequest = _reflection.GeneratedProtocolMessageType('MsgRequest', (_message.Message,), {
  'DESCRIPTOR' : _MSGREQUEST,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:MsgRequest)
  })
_sym_db.RegisterMessage(MsgRequest)

MsgResponse = _reflection.GeneratedProtocolMessageType('MsgResponse', (_message.Message,), {
  'DESCRIPTOR' : _MSGRESPONSE,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:MsgResponse)
  })
_sym_db.RegisterMessage(MsgResponse)



_MSGSERVICE = _descriptor.ServiceDescriptor(
  name='MsgService',
  full_name='MsgService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=84,
  serialized_end=135,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetMsg',
    full_name='MsgService.GetMsg',
    index=0,
    containing_service=None,
    input_type=_MSGREQUEST,
    output_type=_MSGRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_MSGSERVICE)

DESCRIPTOR.services_by_name['MsgService'] = _MSGSERVICE

# @@protoc_insertion_point(module_scope)
