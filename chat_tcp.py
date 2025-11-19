import asyncio
from Chat_store import store
import json

open_connections = []
chats = []
async def handle_client(reader, writer):
    open_connections.append(writer)
    while True:
        data = await reader.readline()
        if not data:
            print("Peer Disconnected")
            break
        chats.append(data.decode().strip())
        print(f"{data.decode().strip()}")

    open_connections.remove(writer)
    writer.close()
    await writer.wait_closed()
    


async def run_server(your_port):
    server = await asyncio.start_server(handle_client, "127.0.0.1", your_port)
    #print(f"[LISTENING on {your_port}]") 
   # print("Waiting for peer....")
    
    return server








async def run_client(your_username, peer_username, peer_port, refresh):
    reader = writer = None
    while True:
        try:
            if not reader:
                reader, writer = await asyncio.open_connection("127.0.0.1", peer_port)
                
                print(f"Successfully connected to {peer_username}")
                #writer.write((your_username + " has connected!\n").encode())
                await writer.drain()
                
                #asyncio.create_task(read_server(reader))
            
            msg = await asyncio.get_event_loop().run_in_executor(None, input)
            if msg == "q":
                writer.close()
                await writer.wait_closed()
                
               
                break
            else:
                writer.write((your_username + ":" + msg + "\n").encode())
                chats.append(f"{your_username}: {msg}")
                await writer.drain()
        except ConnectionRefusedError:
            #print(f"[WAITING FOR PEER] on {peer_port}")
            peer_port = await refresh(peer_username)
            await asyncio.sleep(2)



async def start_chat(your_username,your_port, peer_username, peer_port, refresh, node):
    
    load_users = await node.get("users")

    
    user_dict = json.loads(load_users)
    user_dict[your_username]["chats"].setdefault(peer_username, [])
    if not isinstance(user_dict[your_username]["chats"][peer_username], list):
        user_dict[your_username]["chats"][peer_username] = []

    for x in user_dict[your_username]["chats"][peer_username]:
        print(x)
    await node.set("users", json.dumps(user_dict))

    server = await run_server(your_port)
    asyncio.create_task(server.serve_forever())

    await run_client(your_username,peer_username, peer_port, refresh)

    server.close()

    for x in open_connections:
        x.close()
        await x.wait_closed()
    await store(node, chats, your_username, peer_username)
    open_connections.clear()
    return 
    


    

