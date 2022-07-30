from dataclasses import dataclass, field

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Trx:
    group_id: str
    trx_id: str
    data: bytes
    trx_type: str


@dataclass_json
@dataclass
class Block:
    block_id: str
    group_id: str
    timestamp: str
    producer_pubkey: str
    signature: str
    trxs: list[Trx] = field(default_factory=lambda: [])
    prev_block_id: str = ""
    previous_hash: str = ""
