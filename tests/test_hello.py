from lightnode import LightNode
from lightnode.utils import pretty_print


def test_init_lightnode():
    lightnode = LightNode("/tmp/lightnode")
    assert not lightnode.list_group_seeds()
