from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ImageStreamRequest(_message.Message):
    __slots__ = ("connection_string", "UserName", "Password", "FramePerSecond")
    CONNECTION_STRING_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FRAMEPERSECOND_FIELD_NUMBER: _ClassVar[int]
    connection_string: str
    UserName: str
    Password: str
    FramePerSecond: int
    def __init__(self, connection_string: _Optional[str] = ..., UserName: _Optional[str] = ..., Password: _Optional[str] = ..., FramePerSecond: _Optional[int] = ...) -> None: ...

class ImageResponse(_message.Message):
    __slots__ = ("ImageData",)
    IMAGEDATA_FIELD_NUMBER: _ClassVar[int]
    ImageData: bytes
    def __init__(self, ImageData: _Optional[bytes] = ...) -> None: ...
