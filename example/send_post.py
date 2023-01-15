import os
from datetime import datetime

from lightnode import LightNode

lightnode = LightNode("/tmp/lightnode")
group_id = os.environ["GROUP_ID"]
private_key = bytes.fromhex(os.environ["ETH_PRIV_KEY_HEX"])
obj = {
    "type": "Note",
    "content": "test 2 .. " + datetime.now().isoformat(),
}
print(lightnode.post_to_group(group_id, private_key, obj))
