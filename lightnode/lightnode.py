import pathlib
from typing import Any
from urllib.parse import urljoin

import requests

from .seed import decode_group_seed
from .storage import LocalSeed
from .trx import prepare_send_trx
from .type import DecodeGroupSeedResult
from .utils import get_logger

logger = get_logger("lightnode")


class LightNode:
    def __init__(self, data_dir: str) -> None:
        self.data_dir = pathlib.Path(data_dir).absolute()
        self.localseed = LocalSeed(self.data_dir.as_posix())

        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def encode_group_seed():
        pass

    @staticmethod
    def decode_group_seed(seed_url: str) -> DecodeGroupSeedResult:
        return decode_group_seed(seed_url)

    def join_group(self, seed_url: str) -> None:
        seed = self.decode_group_seed(seed_url)
        self.localseed.save_seed(seed)

    def get_group_seed(self, group_id: str) -> DecodeGroupSeedResult | None:
        return self.localseed.seeds.get(group_id)

    def send_trx(
        self, group_id: str, private_key: bytes, obj: dict[str, Any]
    ) -> str | None:
        if not obj:
            raise ValueError("empty obj")
        if not isinstance(obj, dict):
            raise ValueError("obj should be a dict object")
        if "type" not in obj or "content" not in obj:
            raise ValueError("type and content must in obj")

        seed = self.localseed.seeds.get(group_id)
        if not seed:
            logger.error(
                "can not find group seed from local storage by group_id: %s", group_id
            )
            return

        aes_key = bytes.fromhex(seed.seed.cipher_key)
        trx_obj = prepare_send_trx(group_id, aes_key, private_key, obj)
        print(trx_obj)

        if not isinstance(seed.chain_urls, list) or not seed.chain_urls:
            logger.error("can not find chain api")
            return

        chain_api = seed.chain_urls[0]
        assert chain_api.baseurl.startswith("http")
        assert chain_api.jwt

        url = urljoin(chain_api.baseurl, f"/api/v1/node/trx/{group_id}")
        headers = {
            "Authorization": f"Bearer {chain_api.jwt}",
        }
        req = requests.post(url, json=trx_obj, headers=headers)
        resp = req.json()
        logger.debug("send_trx response: %s", resp)
        return resp.get("trx_id")

    def get_contents(self) -> None:
        pass
