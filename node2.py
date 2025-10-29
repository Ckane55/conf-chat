import asyncio
from kademlia.network import Server
import socket
import bcrypt
import json
node = Server()
async def run():
    # Create a node and start listening on port 5678
    
    await node.listen(5679)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    # Bootstrap the node by connecting to other known nodes, in this case
    # replace 123.123.123.123 with the IP of another node and optionally
    # give as many ip/port combos as you can for other nodes.
    await node.bootstrap([("10.5.0.2", 5678)])
    await login()

    

    


async def login():
    
    answer = input("Returning User? Y/N ")

    if answer == "Y":
        usrname = input("Enter Username:")
        psswrd = input("Enter Password:")
        users = await node.get("users")
        users = json.loads(users)

        login_info = users.get(usrname)
        if bcrypt.checkpw(psswrd.encode(), login_info.get("password").encode()):
            print("WELCOME")
        
        else:
            print("WRONG PASSWORD")








asyncio.run(run())