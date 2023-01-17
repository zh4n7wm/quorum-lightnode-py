import os

from lightnode import LightNode
from lightnode.utils import pretty_print

lightnode = LightNode("/tmp/lightnode")
group_id = os.environ["GROUP_ID"]
age_priv_key = os.environ["ENCRYPT_PRIVARE_KEY"]
trx_id = "7c6da420-59b6-42e6-8794-894c793e735f"
pretty_print(lightnode.get_trx(group_id, trx_id, age_priv_key))
