from lightnode import LightNode
from lightnode.utils import pretty_print

lightnode = LightNode("/tmp/lightnode")
pretty_print(lightnode.list_group_seeds())
