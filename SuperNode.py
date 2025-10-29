
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
    await node.listen(5678)

    await node.bootstrap([("10.5.0.2", 5678)])

    try:
        with open("data.json") as f:
            data = json.load(f)

    except FileNotFoundError:
       print("ERROR")
    
    await node.set("users", json.dumps(data["users"]))



        



    while True:
       await asyncio.sleep(3600)

   
                
        


asyncio.run(run())