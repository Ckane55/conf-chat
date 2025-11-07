import asyncio
from kademlia.network import Server
import socket
import bcrypt
import json
import os
from chat_tcp import run_server, start_chat, run_client
node = Server()
IP = "127.0.0.1"
async def run():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    port = 6000#sock.getsockname()[1]
    sock.close()
    print(f"node 1's port is {port}")
    
    await node.listen(port)

    await node.bootstrap([("127.0.0.1", 5678)])
    

    your_username = await login(port)

    await choice(your_username, port)

    

    
  


   


    

    


async def login(your_port):
    #Grab users from DHT
    load_users = await node.get("users")

    #Convert DHT data to JSON
    user_dict = json.loads(load_users)
    usrname = ""
    
    loop = asyncio.get_running_loop()
    answer = "Y"#await loop.run_in_executor(None, input, "Returning User? Y/N ")
   
   
    if answer == "Y":

        usrname = "Caden"#await loop.run_in_executor(None,input,"Enter Username:")
        while True:
            psswrd = "123"#await loop.run_in_executor(None,input,"Enter Password:")
            
            login_info = user_dict.get(usrname)

            if bcrypt.checkpw(psswrd.encode(), login_info.get("password").encode()):

                
                #Edit JSON to add the port you are currently using
                user_dict[usrname]["port"] = your_port
                
                #set the current JSON
                await node.set("users",json.dumps(user_dict))

                
                
                
                return usrname
                
                
            
            else:

                print("Password is incorrect")
    

    

    



    


    

    '''
    elif answer == "N":
        
        while True:

            setUsername = input("Set Username: ")

            if user_dict.get(setUsername) is not None:

                print("Username is already taken")

            else:

                break
                setPassword = input("Set Password: ")

        salt = bcrypt.gensalt()
        
        #.encode() converts string to bytes and the bytes are hashed
        hash_pw = bcrypt.hashpw(setPassword.encode(),salt)

        #.decode converts the bytes back to a string and the hash string is stored in DHT
        user_dict[setUsername] = {
            "password": hash_pw.decode(),
            "port": port,
            "chats": {}

        }


    
    '''            
    
        
    
    #await node.set("users",json.dumps(user_dict))
   # await check_chats(usrname)
        


"""
async def check_chats(username):
    os.system('cls')
    load_users = await node.get("users")
    user_dict = json.loads(load_users)
    user_chats = user_dict[username]["chats"]

    chats = []
    index = 0
    if user_chats == {}:
        print("You have no active chats")
    else:
        for partner, messages in user_chats.items():
            print(f"#{index} Chat with {partner}")
            chats.append(partner)
    
    choice = input("Choose a chat: ")

    print("To quit type :wq")


    
    user_chat = user_chats[choice]
    port = int(user_dict[choice]["port"])
    


   # os.system('cls')
    #for msg in user_chat:
       # print(print(f"{msg['sender']}: {msg['message']}"))

    
    """

async def choice(your_username, your_port):
        while True:
            print("What next?\n1. Chat with a peer.")

            loop = asyncio.get_running_loop()
            answer = await loop.run_in_executor(None, input, "Pick a number: ")

            if answer == "1":
                #Grab users from DHT
                load_users = await node.get("users")

                #Convert DHT data to JSON
                user_dict = json.loads(load_users)

                print("Peers available to chat:\n")

                for i,users in enumerate(user_dict):
                    print(f"{i}.{users}")
            peer_username = "Chris"#await loop.run_in_executor(None, input, "Pick a peer: ")

            user_dict[your_username]["chats"].setdefault(peer_username, {})

            await node.set("users",json.dumps(user_dict))


            while True:
                if user_dict[peer_username]["port"] == None:
                    print("Cannot find user port")
                    load_users = await node.get("users")

                    #Convert DHT data to JSON
                    user_dict = json.loads(load_users)
                    await asyncio.sleep(2)
                    continue
                else:

                    peer_port = int(user_dict[peer_username]["port"])
                    break
            await start_chat(your_username,your_port, peer_username, peer_port, refresh, node)




async def refresh(peer_username):
    load_users = await node.get("users")

    #Convert DHT data to JSON
    user_dict = json.loads(load_users)
    port = user_dict[peer_username]["port"]
    return port
asyncio.run(run())