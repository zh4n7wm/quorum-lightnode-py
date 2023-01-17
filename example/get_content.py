import os

from lightnode import LightNode
from lightnode.utils import pretty_print

lightnode = LightNode("/tmp/lightnode")
group_id = os.environ["GROUP_ID"]
age_priv_key = os.environ["ENCRYPT_PRIVARE_KEY"]
pretty_print(
    lightnode.get_group_contents(group_id, count=10, age_priv_key=age_priv_key)
)
