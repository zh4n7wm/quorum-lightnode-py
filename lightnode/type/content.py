from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from .object import Object


@dataclass_json
@dataclass
class EncryptedContent:
    Data: str
    Expired: int
    GroupId: str
    SenderPubkey: str
    SenderSign: str
    TimeStamp: int
    TrxId: int
    Version: str


@dataclass_json
@dataclass
class Content:
    Data: Object
    Expired: int
    GroupId: str
    SenderPubkey: str
    SenderSign: str
    TimeStamp: int
    TrxId: int
    Version: str
    Nonce: Optional[int] = None
