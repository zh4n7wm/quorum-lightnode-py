import base64
import hashlib
import json
import time
import uuid
from typing import Any, Dict

import eth_keys
from google.protobuf import any_pb2

from .pb import quorum_pb2 as pbQuorum
from .utils import aes_decrypt, aes_encrypt, get_logger

logger = get_logger("trx")
nonce = 1


def decode_trx_data(
    aes_key: bytes, data: str
) -> pbQuorum.Object:  # pylint: disable=no-member
    """
    1. curl 调用 POST /api/v1/group/content 发 post
    2. curl 调用 GET /api/v1/trx/:group_id/:trx_id 获取刚发的 Data 数据
    3. 然后通过下面代码解出来
    """
    trx_data = b""
    if isinstance(data, str):
        trx_data = data.encode()
    elif isinstance(data, bytes):
        trx_data = data

    trx_enc_bytes = base64.b64decode(trx_data)
    trx_bytes = aes_decrypt(aes_key, trx_enc_bytes)
    any_obj = any_pb2.Any().FromString(trx_bytes)  # pylint: disable=no-member
    obj = pbQuorum.Object()  # pylint: disable=no-member
    any_obj.Unpack(obj)
    return obj


def get_sender_pubkey(private_key: bytes) -> str:
    pk = eth_keys.keys.PrivateKey(private_key)
    return base64.urlsafe_b64encode(pk.public_key.to_compressed_bytes()).decode()


def prepare_send_trx(  # pylint: disable=too-many-locals
    group_id: str, aes_key: bytes, private_key: bytes, obj: Dict[str, Any]
) -> Dict[str, str]:
    obj_pb = pbQuorum.Object(**obj)  # pylint: disable=no-member
    any_obj_pb = any_pb2.Any()  # pylint: disable=no-member
    any_obj_pb.Pack(obj_pb, type_url_prefix="type.googleapis.com/")
    logger.debug("protobuf object: %s", any_obj_pb)

    data = any_obj_pb.SerializeToString()
    encrypted = aes_encrypt(aes_key, data)

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
        "Version": "1.0.0",
        "Expired": int((now + 30) * 1e9),
        "Nonce": nonce,
        "SenderPubkey": sender_pubkey,
    }
    logger.debug("trx object: %s", trx)

    trx_without_sign_pb = pbQuorum.Trx(**trx)  # pylint: disable=no-member
    trx_without_sign_pb_bytes = trx_without_sign_pb.SerializeToString()
    _hash = hashlib.sha256(trx_without_sign_pb_bytes).digest()
    signature = priv.sign_msg_hash(_hash).to_bytes()
    trx["SenderSign"] = signature

    trx_pb = pbQuorum.Trx(**trx)  # pylint: disable=no-member
    trx_json_str = json.dumps(
        {
            "TrxBytes": base64.b64encode(trx_pb.SerializeToString()).decode(),
        }
    )
    logger.debug("trx protobuf: %s", trx_pb)
    enc_trx_json = aes_encrypt(aes_key, trx_json_str.encode())

    send_trx_obj = {
        "GroupId": group_id,
        "TrxItem": base64.b64encode(enc_trx_json).decode(),
    }
    return send_trx_obj
