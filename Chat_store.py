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
    
    if not isinstance(user_dict[your_username]["chats"][peer_username], list):
        user_dict[your_username]["chats"][peer_username] = []

    
    for x in chats:

        user_dict[your_username]["chats"][peer_username].append(x)
    await node.set("users", json.dumps(user_dict))

    print(user_dict)
    
async def offline_store(node, chats, your_username, peer_username):
    load_users = await node.get("users")

    #Convert DHT data to JSON
    user_dict = json.loads(load_users)

    user_dict[your_username]["chats"].setdefault(peer_username, [])
    user_dict[peer_username]["chats"].setdefault(your_username, [])
    
    if not isinstance(user_dict[your_username]["chats"][peer_username], list):
        user_dict[your_username]["chats"][peer_username] = []

    if not isinstance(user_dict[peer_username]["chats"][your_username], list):
        user_dict[your_username]["chats"][peer_username] = []

    
    for x in chats:

        user_dict[your_username]["chats"][peer_username].append(x)
        user_dict[peer_username]["chats"][your_username].append(f"{your_username}: {x}")
    await node.set("users", json.dumps(user_dict))

    print(user_dict)
    