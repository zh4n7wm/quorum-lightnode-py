import os

from lightnode import LightNode
from lightnode.utils import pretty_print

lightnode = LightNode("/tmp/lightnode")
group_id = os.environ["GROUP_ID"]
age_priv_key = os.environ["ENCRYPT_PRIVARE_KEY"]
trx_id = "ada9d298-2f1b-49ec-bd9e-ba2f0702afa8"
pretty_print(lightnode.get_trx(group_id, trx_id, age_priv_key))
