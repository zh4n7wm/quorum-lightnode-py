import os
import secrets

import eth_keys

from lightnode import LightNode
from lightnode.utils import pretty_print
from pyrage import x25519

lightnode = LightNode("/tmp/lightnode")
group_id = os.environ["GROUP_ID"]
age_identity = x25519.Identity.generate()
age_priv_key = str(age_identity)
age_pub_key = str(age_identity.to_public())
eth_priv_key = eth_keys.keys.PrivateKey(secrets.token_bytes(32)).to_bytes()
pretty_print(
    lightnode.announce(
        age_pub_key, eth_priv_key, group_id, "add", "user", "test announce user"
    )
)
