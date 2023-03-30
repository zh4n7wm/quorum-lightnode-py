import base64
import json
import hashlib
import time
from typing import Union, Dict, Any

from lightnode.utils import aes_encrypt

from .pb import quorum_pb2 as pbQuorum
from google.protobuf.json_format import MessageToJson, MessageToDict
import eth_keys


def get_announce_param(
    aes_key: bytes,
    encrypt_pubkey: str,
    private_key: bytes,
    group_id: str,
    action: str,
    _type: str,
    memo: Union[str, None] = None,
) -> dict[str, dict[str, Any]]:
    eth_priv = eth_keys.keys.PrivateKey(private_key)

    item = pbQuorum.AnnounceItem()
    item.GroupId = group_id
    if _type == "user":
        item.Type = pbQuorum.AS_USER
    elif _type == "producer":
        item.Type = pbQuorum.AS_PRODUCER
    else:
        raise ValueError("unsupport type")

    if action == "add":
        item.Action = pbQuorum.ADD
    elif action == "remove":
        item.Action = pbQuorum.REMOVE
    else:
        raise ValueError("unsupport action")

    item.SignPubkey = base64.b64encode(eth_priv.public_key.to_bytes()).decode()
    if item.Type == pbQuorum.AS_USER:
        item.EncryptPubkey = encrypt_pubkey

    item.OwnerPubkey = ""
    item.OwnerSignature = ""
    item.Result = pbQuorum.ANNOUNCED

    data = (
        item.GroupId
        + item.SignPubkey
        + item.EncryptPubkey
        + pbQuorum.AnnounceType.Name(item.Type)
    ).encode()
    _hash = hashlib.sha256(data).digest()
    signature = eth_priv.sign_msg_hash(_hash).to_bytes()

    item.AnnouncerSignature = signature.hex()
    item.TimeStamp = int(time.time() * 1e6)
    if memo:
        item.Memo = memo

    payload = {
        "data": MessageToDict(item),
    }
    return payload
