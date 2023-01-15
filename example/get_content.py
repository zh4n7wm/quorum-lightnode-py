import os

from lightnode import LightNode

lightnode = LightNode("/tmp/lightnode")
group_id = os.environ["GROUP_ID"]
print(lightnode.get_group_contents(group_id, count=10))
