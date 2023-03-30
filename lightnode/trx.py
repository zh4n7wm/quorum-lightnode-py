import base64
import hashlib
import json
import time
import uuid
from typing import Any, Dict, List, Union

import eth_keys

from .pb import quorum_pb2 as pbQuorum
from .utils import (
    aes_decrypt,
    aes_encrypt,
    age_decrypt,
    age_encrypt,
    age_privkey_from_str,
    get_logger,
)

logger = get_logger("trx")
nonce = 1


def decode_public_trx_data(aes_key: bytes, data: str):
    return decode_trx_data(aes_key, None, data)


def decode_private_trx_data(age_key: str, data: str):
    return decode_trx_data(None, age_key, data)


def decode_trx_data(
    aes_key: Union[bytes, None], age_priv_key: Union[str, None], data: str
) -> pbQuorum.Object:  # pylint: disable=no-member
    trx_data = b""
    if isinstance(data, str):
        trx_data = data.encode()
    elif isinstance(data, bytes):
        trx_data = data

    trx_enc_bytes = base64.b64decode(trx_data)
    trx_bytes = None
    if aes_key:
        trx_bytes = aes_decrypt(aes_key, trx_enc_bytes)
    elif age_priv_key:
        age_key = age_privkey_from_str(age_priv_key)
        trx_bytes = age_decrypt(age_key, trx_enc_bytes)
    else:
        raise ValueError("aes_key and age_key both empty")

    return trx_bytes


def get_sender_pubkey(private_key: bytes) -> str:
    pk = eth_keys.keys.PrivateKey(private_key)
    return base64.urlsafe_b64encode(pk.public_key.to_compressed_bytes()).decode()


def prepare_send_trx(  # pylint: disable=too-many-locals
    group_id: str,
    aes_key: bytes,
    private_key: bytes,
    obj: Dict[str, Any],
    recipients: Union[List[str], None],
) -> Dict[str, str]:
    data = json.dumps(obj).encode()
    encrypted = None
    if not recipients:
        encrypted = aes_encrypt(aes_key, data)
    else:
        encrypted = age_encrypt(recipients, data)

    priv = eth_keys.keys.PrivateKey(private_key)
    sender_pubkey = get_sender_pubkey(private_key)

    now = time.time()
    global nonce
    nonce += 1
    trx = {
        "TrxId": str(uuid.uuid4()),
        "GroupId": group_id,
        "Data": encrypted,
        "TimeStamp": int(now * 1e9),
        "Version": "2.0.0",
        "SenderPubkey": sender_pubkey,
    }
    logger.debug("trx object: %s", trx)

    trx_without_sign_pb = pbQuorum.Trx(**trx)  # pylint: disable=no-member
    trx_without_sign_pb_bytes = trx_without_sign_pb.SerializeToString()
    _hash = hashlib.sha256(trx_without_sign_pb_bytes).digest()
    signature = priv.sign_msg_hash(_hash).to_bytes()
    trx["SenderSign"] = signature

    # Note: for rest api payload
    _trx = {
        "group_id": trx["GroupId"],
        "trx_id": trx["TrxId"],
        "data": base64.b64encode(trx["Data"]).decode(),
        "timestamp": str(trx["TimeStamp"]),
        "version": trx["Version"],
        "sender_pubkey": trx["SenderPubkey"],
        "sender_sign": base64.b64encode(trx["SenderSign"]).decode(),
    }

    return _trx
