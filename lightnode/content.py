import base64
import json
from typing import Union, Dict

from .utils import aes_encrypt


def get_content_param(
    aes_key: bytes,
    group_id: str,
    start_trx: Union[str, None] = None,
    count: int = 20,
    reverse: bool = False,
) -> Dict[str, str]:
    params = {
        "group_id": group_id,
        "reverse": reverse,
        "num": count,
        "include_start_trx": False,
        # "senders": [],
    }
    if start_trx:
        params["start_trx"] = start_trx

    return params
