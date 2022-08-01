import copy
import json
import pathlib

from ..seed import parse_chain_url
from ..type import ChainURL, DecodeGroupSeedResult
from ..utils import get_logger, json_dump

logger = get_logger("storage.seed")


class LocalSeed:
    def __init__(self, save_dir: str) -> None:
        self.save_dir = save_dir
        self.save_path = pathlib.Path(self.save_dir) / "seed.json"
        self.seeds: dict[str, DecodeGroupSeedResult] = self._load()

    def _load(self) -> dict[str, DecodeGroupSeedResult]:
        local_seeds = {}

        if not pathlib.Path(self.save_path).exists():
            return local_seeds

        with open(self.save_path, encoding="utf-8") as fp:

            data = json.load(fp)
            if not isinstance(data, dict):
                raise ValueError("local seeds is not a dict object")
            for k, v in data.items():
                # pylint: disable=no-member
                local_seeds[k] = DecodeGroupSeedResult.from_dict(v)
            return local_seeds

    def _dump(self) -> None:
        with open(self.save_path, "w", encoding="utf-8") as fp:
            json_dump(self.seeds, fp)

    def save_seed(self, seed: DecodeGroupSeedResult) -> None:
        self.seeds[seed.seed.group_id] = seed
        self._dump()

    def remove_seed(self, group_id: str) -> None:
        if group_id not in self.seeds:
            raise ValueError("not found group")
        del self.seeds[group_id]
        self._dump()

    def get_all_seeds(self) -> dict[str, DecodeGroupSeedResult]:
        return self.seeds

    def get_seed(self, group_id: str) -> DecodeGroupSeedResult:
        seed = self.seeds.get(group_id)
        if not seed:
            raise ValueError("group not found")
        return seed

    def get_chain_urls(self, group_id: str) -> list[ChainURL]:
        seed = self.get_seed(group_id)
        return seed.chain_urls

    def update_chain_url(self, group_id: str, chain_url: str) -> None:
        seed = self.seeds.get(group_id)
        if not seed:
            logger.warning("can not find local group seed by group_id: %s", group_id)
            return

        chain_api = parse_chain_url(chain_url)
        if not chain_api.baseurl or not chain_api.jwt:
            logger.error("invalid chain api url: %s", chain_api)
            return

        chain_urls: list[ChainURL] = copy.deepcopy(seed.chain_urls)
        # Note: remove exist chain url
        for x in seed.chain_urls:
            if x.baseurl.lower() == chain_api.baseurl.lower():
                chain_urls.remove(x)
        chain_urls.insert(0, chain_api)
        seed.chain_urls = chain_urls
