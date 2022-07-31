from lightnode import LightNode

lightnode = LightNode("/tmp/lightnode")
group_id = "07c54a75-4db7-4f91-96c0-33d91a96c36f"
print(lightnode.get_contents(group_id, count=2))
