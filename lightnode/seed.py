import base64
import hashlib
import uuid
from urllib.parse import parse_qs, unquote, urlparse

from .pb import quorum_pb2 as pbQuorum
from .type import ChainURL, DecodeGroupSeedResult, GroupSeed


def urlsafe_b64decode(s: bytes | str) -> bytes:
    if isinstance(s, str):
        s = s.encode()
    return base64.urlsafe_b64decode(s + b"=" * (len(s) % 4))


def _get_value_from_query(query: dict, key: str) -> str:
    val = query.get(key)
    if not val:
        raise KeyError("can not find key or value is empty")
    if not isinstance(val, list):
        raise ValueError("value is not a list")

    return val[0]


def extract_uuid_from_query(query: dict, key: str) -> str:
    val = _get_value_from_query(query, key)
    b = urlsafe_b64decode(val)
    return str(uuid.UUID(bytes=b))


def extra_timestamp_from_query(query: dict, key: str) -> int:
    val = _get_value_from_query(query, key)
    t = urlsafe_b64decode(val.encode())
    timestamp = int.from_bytes(t, byteorder="big")
    return timestamp


def hash_block(block: pbQuorum.Block) -> bytes:  # pylint: disable=no-member
    new_block = pbQuorum.Block()  # pylint: disable=no-member
    new_block.CopyFrom(block)
    new_block.Hash = b""
    new_block.Signature = b""
    new_block_bytes = new_block.SerializeToString()
    return hashlib.sha256(new_block_bytes).digest()


def parse_chain_url(url: str) -> ChainURL:
    u = urlparse(url)
    baseurl = f"{u.scheme}://{u.hostname}:{u.port}"
    query = parse_qs(u.query)
    jwt = _get_value_from_query(query, "jwt")
    return ChainURL(baseurl=baseurl, jwt=jwt)


def decode_group_seed(seed_url: str) -> DecodeGroupSeedResult:
    u = urlparse(seed_url)
    assert u.scheme == "rum"
    assert u.netloc == "seed"
    assert u.path == ""

    query = parse_qs(u.query)
    group_id = extract_uuid_from_query(query, "g")

    genesis_block = pbQuorum.Block(  # pylint: disable=no-member
        BlockId=extract_uuid_from_query(query, "b"),
        GroupId=group_id,
        TimeStamp=extra_timestamp_from_query(query, "t"),
        PrevBlockId="",
        PreviousHash=b"",
        ProducerPubKey=_get_value_from_query(query, "k"),
        Trxs=None,
        Signature=urlsafe_b64decode(_get_value_from_query(query, "s")),
    )
    genesis_block.Hash = hash_block(genesis_block)

    consensus_type = "pos" if _get_value_from_query(query, "n") == "1" else "poa"
    encryption_type = (
        "public" if _get_value_from_query(query, "e") == "0" else "private"
    )
    seed = GroupSeed(
        genesis_block=genesis_block,
        group_id=group_id,
        group_name=_get_value_from_query(query, "a"),
        consensus_type=consensus_type,
        encryption_type=encryption_type,
        cipher_key=urlsafe_b64decode(_get_value_from_query(query, "c")).hex(),
        owner_pubkey=genesis_block.ProducerPubKey,
        signature=genesis_block.Signature.hex(),
        app_key=unquote(_get_value_from_query(query, "y")),
    )

    chain_urls = []
    urls = list(set(_get_value_from_query(query, "u").split("|")))
    for url in urls:
        item = parse_chain_url(url)
        chain_urls.append(item)

    return DecodeGroupSeedResult(seed=seed, chain_urls=chain_urls)
