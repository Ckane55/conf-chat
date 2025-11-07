import asyncio
from kademlia.network import Server
import socket
import bcrypt
import json
node = Server()
async def run():

    
    await node.listen(5679)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)


    await node.bootstrap([("127.0.0.1", 5678)])

    users = await node.get("users")
    print(users)



asyncio.run(run())