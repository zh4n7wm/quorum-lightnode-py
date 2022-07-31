import base64
import json

from .utils import aes_encrypt


def get_content_param(
    aes_key: bytes,
    group_id: str,
    start_trx: str | None = None,
    count: int = 20,
    reverse: bool = False,
) -> dict[str, str]:
    params = {
        "group_id": group_id,
        "reverse": "true" if reverse is True else "false",
        "num": count,
        "include_start_trx": "false",
        "senders": [],
    }
    if start_trx:
        params["start_trx"] = start_trx

    get_group_ctn_item = {
        "Req": params,
    }

    get_group_ctn_item_str = json.dumps(get_group_ctn_item)
    encrypted = aes_encrypt(aes_key, get_group_ctn_item_str.encode())
    send_param = {
        "Req": base64.b64encode(encrypted).decode(),
    }

    return send_param
