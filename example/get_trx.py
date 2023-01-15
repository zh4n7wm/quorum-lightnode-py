import os

from lightnode import LightNode

lightnode = LightNode("/tmp/lightnode")
group_id = os.environ["GROUP_ID"]
trx_id = "dc13822b-ddbc-4e8b-b279-4be444396fe8"
print(lightnode.get_trx(group_id, trx_id))
