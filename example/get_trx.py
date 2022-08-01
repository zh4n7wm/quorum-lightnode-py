from lightnode import LightNode

lightnode = LightNode("/tmp/lightnode")
group_id = "07c54a75-4db7-4f91-96c0-33d91a96c36f"
trx_id = "0018bf34-f430-4e3e-9d65-f2a328385e91"
print(lightnode.get_trx(group_id, trx_id))
