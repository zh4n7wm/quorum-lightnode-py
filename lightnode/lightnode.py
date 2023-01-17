import json
import pathlib
from typing import Any
from urllib.parse import urljoin

import requests

from .content import get_content_param
from .seed import decode_group_seed
from .storage import LocalSeed
from .trx import decode_private_trx_data, decode_public_trx_data, prepare_send_trx
from .type import Content, DecodeGroupSeedResult
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

    def leave_group(self, group_id: str) -> None:
        self.localseed.remove_seed(group_id)

    def get_group_seed(self, group_id: str) -> DecodeGroupSeedResult:
        if group_id not in self.localseed.seeds:
            raise ValueError("group not found")
        return self.localseed.seeds[group_id]

    def list_group_seeds(self) -> dict[str, DecodeGroupSeedResult]:
        return self.localseed.get_all_seeds()

    def update_chain_api(self, group_id: str, chain_url: str) -> None:
        self.localseed.update_chain_url(group_id, chain_url)

    def get_encrypt_pub_keys(self, group_id: str) -> list[str]:
        chain_url = self.localseed.get_chain_urls(group_id)[0]
        url = urljoin(chain_url.baseurl, f"/api/v1/node/getencryptpubkeys/{group_id}")
        headers = {
            "Authorization": f"Bearer {chain_url.jwt}",
        }
        req = requests.get(url, headers=headers)
        req.raise_for_status()
        data = req.json()
        return data.get("keys")

    def get_trx(
        self, group_id: str, trx_id: str, age_priv_key: str | None = None
    ) -> dict[str, Any]:
        seed = self.get_group_seed(group_id)
        chain_url = self.localseed.get_chain_urls(group_id)[0]
        url = urljoin(chain_url.baseurl, f"/api/v1/trx/{group_id}/{trx_id}")
        headers = {
            "Authorization": f"Bearer {chain_url.jwt}",
        }
        req = requests.get(url, headers=headers)
        req.raise_for_status()
        data = req.json()
        is_private_group = seed.seed.encryption_type == "private"
        if is_private_group:
            if not age_priv_key:
                raise ValueError("empty age key for private group")
            obj = decode_private_trx_data(age_priv_key, data["Data"].encode())
        else:
            aes_key = bytes.fromhex(seed.seed.cipher_key)
            obj = decode_public_trx_data(aes_key, data["Data"].encode())
        trx = {**data, "Data": json.loads(obj)}
        return trx

    def post_to_group(
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

        is_private_group = seed.seed.encryption_type == "private"
        recipients = None
        if is_private_group:
            recipients = self.get_encrypt_pub_keys(group_id)
            if not recipients:
                logger.error("can not get encrypt recipients")
                return

        aes_key = bytes.fromhex(seed.seed.cipher_key)
        trx_obj = prepare_send_trx(group_id, aes_key, private_key, obj, recipients)
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
        if req.status_code >= 400:
            logger.error("send_trx response: %s", resp)
        else:
            logger.debug("send_trx response: %s", resp)
        return resp.get("trx_id")

    def get_group_contents(  # pylint: disable=too-many-locals disable=too-many-arguments
        self,
        group_id: str,
        start_trx: str | None = None,
        count: int = 20,
        reverse: bool = False,
        age_priv_key: str | None = None,
    ) -> list[dict[str, Any]]:
        seed = self.localseed.seeds.get(group_id)
        if not seed:
            raise ValueError("group not found")

        aes_key = bytes.fromhex(seed.seed.cipher_key)
        payload = get_content_param(aes_key, group_id, start_trx, count, reverse)

        chain_api = seed.chain_urls[0]
        url = urljoin(chain_api.baseurl, f"/api/v1/node/groupctn/{group_id}")
        headers = {
            "Authorization": f"Bearer {chain_api.jwt}",
        }
        req = requests.post(url, json=payload, headers=headers)
        result: list[Content] = []
        is_private_group = seed.seed.encryption_type == "private"
        for item in req.json():
            obj = None
            if not is_private_group:
                obj = decode_public_trx_data(aes_key, item["Data"].encode())
            else:
                if not age_priv_key:
                    raise ValueError("empty age private key for private group")
                obj = decode_private_trx_data(age_priv_key, item["Data"].encode())

            _content = {**item, "Data": json.loads(obj.decode())}
            result.append(_content)
        return result
