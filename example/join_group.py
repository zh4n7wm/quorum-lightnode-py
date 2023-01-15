import os

from lightnode import LightNode

# pylint: disable=line-too-long
seed_url = os.environ["GROUP_SEED"]

lightnode = LightNode("/tmp/lightnode")
lightnode.join_group(seed_url)
seed = lightnode.decode_group_seed(seed_url)
print(lightnode.get_group_seed(seed.seed.group_id))
