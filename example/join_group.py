from lightnode import LightNode

# pylint: disable=line-too-long
seed_url = "rum://seed?v=1\u0026e=0\u0026n=0\u0026b=1c8HT25ST-SXcBGtQ4AkmA\u0026c=0dO7vm0d0sbmE3Gel-_qexjy2J474V_-UepylrbzXg4\u0026g=CbUmuZ2mSAa-dScCqIT26g\u0026k=Ax-Orq3wJ4zOiX1AS6a0q10LgvURNqjY0R6CH11QqQoK\u0026s=3dl9WJlApPxz-FAKdBPoBRIJU0CAHtaUIccG_jHcKbtHl0RU7ts9DKLX1-XfcEyIacJDo-tHkWV3YZds-tE6RAA\u0026t=FwNph_b28ng\u0026a=test_app2\u0026y=test_app2\u0026u=http%3A%2F%2F192.168.50.8%3A8002%3Fjwt%3DeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbGxvd0dyb3VwcyI6WyIwOWI1MjZiOS05ZGE2LTQ4MDYtYmU3NS0yNzAyYTg4NGY2ZWEiXSwiZXhwIjoxODE1OTY1MTIxLCJuYW1lIjoiYWxsb3ctMDliNTI2YjktOWRhNi00ODA2LWJlNzUtMjcwMmE4ODRmNmVhIiwicm9sZSI6Im5vZGUifQ.E_CJ-C_Um4FKV7JJOdsWKefrpZ--Np-BmLJJOQXVDx4|http%3A%2F%2F192.168.50.8%3A8002%3Fjwt%3DeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbGxvd0dyb3VwcyI6WyIwOWI1MjZiOS05ZGE2LTQ4MDYtYmU3NS0yNzAyYTg4NGY2ZWEiXSwiZXhwIjoxODE1OTY1MTIxLCJuYW1lIjoiYWxsb3ctMDliNTI2YjktOWRhNi00ODA2LWJlNzUtMjcwMmE4ODRmNmVhIiwicm9sZSI6Im5vZGUifQ.E_CJ-C_Um4FKV7JJOdsWKefrpZ--Np-BmLJJOQXVDx4"

lightnode = LightNode("/tmp/lightnode")
lightnode.join_group(seed_url)
seed = lightnode.decode_group_seed(seed_url)
print(lightnode.get_group_seed(seed.seed.group_id))
