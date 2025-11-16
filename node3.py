import asyncio
from kademlia.network import Server
import socket
import bcrypt
import json
import os
import sys
from chat_tcp import run_server, start_chat, run_client
node = Server()
IP = "127.0.0.1"
async def run():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    port = 6002#sock.getsockname()[1]
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
    answer = await loop.run_in_executor(None, input, "Returning User? Y/N ")
   
   
    if answer == "Y":

        usrname = await loop.run_in_executor(None,input,"Enter Username:")
        while True:
            psswrd = await loop.run_in_executor(None,input,"Enter Password:")
            
            login_info = user_dict.get(usrname)

            if bcrypt.checkpw(psswrd.encode(), login_info.get("password").encode()):

                
                #Edit JSON to add the port you are currently using
                user_dict[usrname]["port"] = your_port
                user_dict[usrname]["status"] = "online"
                
                #set the current JSON
                await node.set("users",json.dumps(user_dict))

                
                
                
                return usrname
                
                
            
            else:

                print("Password is incorrect")
    
    elif answer == "N":
        
        while True:

            setUsername = input("Set Username: ")

            if user_dict.get(setUsername) is not None:

                print("Username is already taken")

            else:

                
                setPassword = input("Set Password: ")
                break

        salt = bcrypt.gensalt()
        
        #.encode() converts string to bytes and the bytes are hashed
        hash_pw = bcrypt.hashpw(setPassword.encode(),salt)

        #.decode converts the bytes back to a string and the hash string is stored in DHT
        user_dict[setUsername] = {
            "password": hash_pw.decode(),
            "port": your_port,
            "chats": {}

        }


    
              
    
        
    
    await node.set("users",json.dumps(user_dict))
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
                while True:

                    #Grab users from DHT
                    load_users = await node.get("users")

                    #Convert DHT data to JSON
                    user_dict = json.loads(load_users)

                    print("Peers available to chat:\n")

                    for username, info in user_dict.items():
                        if username == your_username:
                            continue
                        elif info.get("status") == "offline":
                            continue
                        else:

                            print(f"{username}")
                    peer_username = await loop.run_in_executor(None, input, "Pick a peer: ")
                    if peer_username == "r":
                        os.system('cls')
                        continue
                    elif peer_username == "q":
                        await quit_app(user_dict ,your_username)

                    else:
                        break


                
            

            

                user_dict[your_username]["chats"].setdefault(peer_username, {})

                await node.set("users",json.dumps(user_dict))

            elif answer == "q":
                #await remove peer
                sys.exit


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


async def quit_app(user_dict, your_username):

    user_dict[your_username]["status"] = "offline"
    await node.set("users", json.dumps(user_dict))

    sys.exit()
asyncio.run(run())

#async def remove
