from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthTokenRequest(_message.Message):
    __slots__ = ("JwtToken",)
    JWTTOKEN_FIELD_NUMBER: _ClassVar[int]
    JwtToken: str
    def __init__(self, JwtToken: _Optional[str] = ...) -> None: ...

class GetUserReply(_message.Message):
    __slots__ = ("FirstName", "LastName", "UserName")
    FIRSTNAME_FIELD_NUMBER: _ClassVar[int]
    LASTNAME_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    FirstName: str
    LastName: str
    UserName: str
    def __init__(self, FirstName: _Optional[str] = ..., LastName: _Optional[str] = ..., UserName: _Optional[str] = ...) -> None: ...

class ValidTokenReply(_message.Message):
    __slots__ = ("IsOkay",)
    ISOKAY_FIELD_NUMBER: _ClassVar[int]
    IsOkay: bool
    def __init__(self, IsOkay: bool = ...) -> None: ...

class ClaimModel(_message.Message):
    __slots__ = ("type", "value")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    type: str
    value: str
    def __init__(self, type: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class ClaimArrayReply(_message.Message):
    __slots__ = ("Claims",)
    CLAIMS_FIELD_NUMBER: _ClassVar[int]
    Claims: _containers.RepeatedCompositeFieldContainer[ClaimModel]
    def __init__(self, Claims: _Optional[_Iterable[_Union[ClaimModel, _Mapping]]] = ...) -> None: ...

class IsAuthorizeRequest(_message.Message):
    __slots__ = ("UserId", "Claim")
    USERID_FIELD_NUMBER: _ClassVar[int]
    CLAIM_FIELD_NUMBER: _ClassVar[int]
    UserId: str
    Claim: str
    def __init__(self, UserId: _Optional[str] = ..., Claim: _Optional[str] = ...) -> None: ...

class IsAuthorizeReply(_message.Message):
    __slots__ = ("Authorized",)
    AUTHORIZED_FIELD_NUMBER: _ClassVar[int]
    Authorized: bool
    def __init__(self, Authorized: bool = ...) -> None: ...

class IsAuthorizedTokenReply(_message.Message):
    __slots__ = ("Authorized",)
    AUTHORIZED_FIELD_NUMBER: _ClassVar[int]
    Authorized: bool
    def __init__(self, Authorized: bool = ...) -> None: ...

class IsAuthorizedTokenRequest(_message.Message):
    __slots__ = ("Token", "Claim")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    CLAIM_FIELD_NUMBER: _ClassVar[int]
    Token: str
    Claim: str
    def __init__(self, Token: _Optional[str] = ..., Claim: _Optional[str] = ...) -> None: ...
