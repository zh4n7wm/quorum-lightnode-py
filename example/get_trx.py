import os

from lightnode import LightNode
from lightnode.utils import pretty_print

lightnode = LightNode("/tmp/lightnode")
group_id = os.environ["GROUP_ID"]
age_priv_key = os.environ["ENCRYPT_PRIVARE_KEY"]
trx_id = os.environ["TRX_ID"]
pretty_print(lightnode.get_trx(group_id, trx_id, age_priv_key))
