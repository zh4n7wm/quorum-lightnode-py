from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from ..pb import quorum_pb2 as pbQuorum


@dataclass_json
@dataclass
class GroupSeed:
    genesis_block: pbQuorum.Block  # pylint: disable=no-member
    group_id: str
    group_name: str
    owner_pubkey: str
    consensus_type: str
    encryption_type: str
    cipher_key: str
    app_key: str
    signature: str


@dataclass_json
@dataclass
class ChainURL:
    baseurl: str
    jwt: str


@dataclass_json
@dataclass
class DecodeGroupSeedResult:
    seed: GroupSeed
    chain_urls: list[ChainURL] = field(default_factory=lambda: [])
