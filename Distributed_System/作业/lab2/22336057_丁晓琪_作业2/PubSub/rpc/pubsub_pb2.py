# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: rpc/pubsub.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'rpc/pubsub.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10rpc/pubsub.proto\"2\n\x10SubscribeRequest\x12\x12\n\ntopic_name\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\"!\n\x11SubscribeResponse\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x05\"\x18\n\nrequest_id\x12\n\n\x02id\x18\x01 \x01(\t\"B\n\rtopic_Message\x12\r\n\x05topic\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\x32q\n\nSubService\x12\x32\n\tSubscribe\x12\x11.SubscribeRequest\x1a\x12.SubscribeResponse\x12/\n\x0eMessage_Stream\x12\x0b.request_id\x1a\x0e.topic_Message0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'rpc.pubsub_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SUBSCRIBEREQUEST']._serialized_start=20
  _globals['_SUBSCRIBEREQUEST']._serialized_end=70
  _globals['_SUBSCRIBERESPONSE']._serialized_start=72
  _globals['_SUBSCRIBERESPONSE']._serialized_end=105
  _globals['_REQUEST_ID']._serialized_start=107
  _globals['_REQUEST_ID']._serialized_end=131
  _globals['_TOPIC_MESSAGE']._serialized_start=133
  _globals['_TOPIC_MESSAGE']._serialized_end=199
  _globals['_SUBSERVICE']._serialized_start=201
  _globals['_SUBSERVICE']._serialized_end=314
# @@protoc_insertion_point(module_scope)
