from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

<<<<<<< HEAD
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
=======
class CameraFrame(_message.Message):
    __slots__ = ("frame",)
    FRAME_FIELD_NUMBER: _ClassVar[int]
    frame: bytes
    def __init__(self, frame: _Optional[bytes] = ...) -> None: ...
>>>>>>> 3b6cd222f12e67a85c831f7eb0dc8aabce2d8e61
