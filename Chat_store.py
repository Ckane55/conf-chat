import asyncio
from kademlia.network import Server
import socket
import bcrypt
import json
import os



async def store(node, chats, your_username, peer_username):

    load_users = await node.get("users")

    #Convert DHT data to JSON
    user_dict = json.loads(load_users)

    user_dict[your_username]["chats"].setdefault(peer_username, [])
    
    
    for x in chats:

        user_dict[your_username]["chats"][peer_username].append(x)
    await node.set("users", json.dumps(user_dict))

    print(user_dict)
    

    