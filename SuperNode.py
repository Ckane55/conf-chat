
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

    await node.bootstrap([("127.0.0.1", 5678)])  # self
    

    try:
        with open("data.json") as f:
            data = json.load(f)

    except FileNotFoundError:
       print("ERROR")
    
    await node.set("users", json.dumps(data["users"]))
    asyncio.create_task(keep_alive(node))

    print("Waiting for connection")
    stop_event = asyncio.Event()
    await stop_event.wait()

async def keep_alive(node):
    while True:
        try:
            # trigger a ping/get to keep routing table active
            await node.get("users")
        except Exception:
            pass
        await asyncio.sleep(10) 
        

asyncio.run(run())