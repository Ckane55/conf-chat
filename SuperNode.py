
import socket
import asyncio
from kademlia.network import Server
import json

async def run():
    node = Server()
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(ip)
    await node.listen(5678)


    
    # set a value for the key "my-key" on the network
    #await node.set("node1", ip)
    while True:
       await asyncio.sleep(3600)
   

asyncio.run(run())