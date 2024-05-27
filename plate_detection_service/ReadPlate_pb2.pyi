from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReadPlateRequest(_message.Message):
    __slots__ = ("guid",)
    GUID_FIELD_NUMBER: _ClassVar[int]
    guid: str
    def __init__(self, guid: _Optional[str] = ...) -> None: ...

class ReadPlateReply(_message.Message):
    __slots__ = ("plate", "image_path")
    PLATE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_PATH_FIELD_NUMBER: _ClassVar[int]
    plate: str
    image_path: str
    def __init__(self, plate: _Optional[str] = ..., image_path: _Optional[str] = ...) -> None: ...
