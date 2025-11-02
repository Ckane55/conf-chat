
import socket
import asyncio
from kademlia.network import Server
import json
import bcrypt
async def run():
    node = Server()
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(ip)
    await node.listen(5679)

    await node.bootstrap([
    ("127.0.0.1", 5679),  # self
    ("127.0.0.1", 5678)   # first supernode
    ])

    try:
        with open("data.json") as f:
            data = json.load(f)

    except FileNotFoundError:
       print("ERROR")
    
    await node.set("users", json.dumps(data["users"]))



        



    while True:
       await asyncio.sleep(5)

   
                
        


asyncio.run(run())