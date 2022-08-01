from lightnode import LightNode

lightnode = LightNode("/tmp/lightnode")
group_id = "07c54a75-4db7-4f91-96c0-33d91a96c36f"
private_key = bytes.fromhex(
    "37e8313252514aef1914aff1751ee8be7935a40fe27458b1d2685f34f5a5f9c3"
)
obj = {
    "type": "Note",
    "content": "test 2 ..",
}
print(lightnode.post_to_group(group_id, private_key, obj))
