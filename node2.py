import asyncio
from kademlia.network import Server
import socket
import bcrypt
import json
node = Server()
async def run():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    
    
    await node.listen(port)
    


    await node.bootstrap([("127.0.0.1", 5678)])
    await login(port)
    while True:
        await asyncio.sleep(5)

    

    


async def login(port):
    load_users = await node.get("users")

    user_dict = json.loads(load_users)
    
    answer = input("Returning User? Y/N ")
    valid = False
   
    if answer == "Y":

        usrname = input("Enter Username:")
        while valid == False:
            psswrd = input("Enter Password:")
            
            login_info = user_dict.get(usrname)

            if bcrypt.checkpw(psswrd.encode(), login_info.get("password").encode()):

                

                user_dict[usrname]["Port"] = port
                await node.set("users",json.dumps(user_dict))
                break
                
                
            
            else:

                print("Password is incorrect")



                
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

    await node.set("users",json.dumps(user_dict))
    await check_chats(usrname)
        







async def check_chats(username):
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
            chats.append(index)

            


asyncio.run(run())