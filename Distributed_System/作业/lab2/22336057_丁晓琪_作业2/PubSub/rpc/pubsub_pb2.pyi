from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SubscribeRequest(_message.Message):
    __slots__ = ("topic_name", "id")
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    id: str
    def __init__(self, topic_name: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class SubscribeResponse(_message.Message):
    __slots__ = ("flag",)
    FLAG_FIELD_NUMBER: _ClassVar[int]
    flag: int
    def __init__(self, flag: _Optional[int] = ...) -> None: ...

class request_id(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class topic_Message(_message.Message):
    __slots__ = ("topic", "content", "timestamp")
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    topic: str
    content: str
    timestamp: int
    def __init__(self, topic: _Optional[str] = ..., content: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...
