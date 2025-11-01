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
    load_users = await node.get("users")

    user_dict = json.loads(load_users)
    
    answer = input("Returning User? Y/N ")
    attempts = 0
   
    if answer == "Y":

        usrname = input("Enter Username:")
        while attempts != 3:
            psswrd = input("Enter Password:")
            
            login_info = user_dict.get(usrname)

            if bcrypt.checkpw(psswrd.encode(), login_info.get("password").encode()):

                print("WELCOME")
                break
            
            else:

                print("Password is incorrect")
                attempts += 1
                if attempts != 3:
                    print("You have " + str(3 - attempts) + " attempts left.")
                else:
                    print("You have reached the maximum amount of password attempts.")
                




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
        user_dict[setUsername] = hash_pw.decode()

        await node.set("users",json.dumps(user_dict))

        


        





    








asyncio.run(run())