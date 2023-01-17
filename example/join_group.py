import os

from lightnode import LightNode
from lightnode.utils import pretty_print

# pylint: disable=line-too-long
seed_url = os.environ["GROUP_SEED"]

lightnode = LightNode("/tmp/lightnode")
lightnode.join_group(seed_url)
seed = lightnode.decode_group_seed(seed_url)
pretty_print(lightnode.get_group_seed(seed.seed.group_id))
