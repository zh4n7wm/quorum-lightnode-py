from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from .object import Object


@dataclass_json
@dataclass
class EncryptedTrx:
    """
    GET /api/v1/trx/{group_id}/{trx_id} response
    """

    TrxId: str
    Type: str
    GroupId: str
    Data: str
    TimeStamp: str
    Version: str
    Expired: str
    ResendCount: str
    SenderPubkey: str
    SenderSign: str
    StorageType: str
    Nonce: Optional[str] = None


@dataclass_json
@dataclass
class Trx:
    """
    GET /api/v1/trx/{group_id}/{trx_id} response
    then decode `Data` to `Object`
    """

    TrxId: str
    Type: str
    GroupId: str
    Data: Object
    TimeStamp: str
    Version: str
    Expired: str
    ResendCount: str
    SenderPubkey: str
    SenderSign: str
    StorageType: str
    Nonce: Optional[str] = None
