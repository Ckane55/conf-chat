# conf-chat
A P2P Chat application made in Python using Kademlia for the DHT and Asyncio for the live TCP chat.


# How it works.

Conf-chat works by storing user data in a distributed hash table that is stored among peer nodes. In a given nodes DHT will be the username and passwords of other users which is stored as a hash using bcrypt. The port that the peer is using will be stored in the DHT upon the user logging in and the current chats that the user has among different peers will also be stored in the table. Each user also has a status associated with them in the table that tells other peers if they are online or offline. If a peer is offline and another user tries to message them, the messages sent will be written to the DHT directly. If the user is online, then a TCP connection will be establishes that allows for live text chat between the two. Upon terminating the TCP connection, the chats are stored in the DHT so that they can be viewed at any time.

Below is a JSON of the DHT structure
<img width="836" height="605" alt="image" src="https://github.com/user-attachments/assets/89cfa6d4-6813-4e3e-9abd-58561a7e1161" />


# How to run it

1. You will need to start supernode.py, this is a bootstrap node that initializes the network that subsequent nodes will connect to the network with
   <img width="540" height="222" alt="image" src="https://github.com/user-attachments/assets/5a1eac53-67c9-4116-a7e7-894f6df5b85d" />

2. You can now startup Node1.py which will connect to the super node and get its DHT data. You can either login or create a user. All pre-initialized users have a password of "123"

3. After you initialize the 1st node you can go and start node2.py and complete the same process as node 1.

4. When you arrive at the user Selection screen (Below) you can select an online or offline user to chat with. You can refresh the list by typing "r" or quit the app by typing "q". To start a TCP connection with a peer enter their username and select enter.

<img width="1137" height="565" alt="image" src="https://github.com/user-attachments/assets/dc822ac8-71e5-48d1-be8d-60283f568c00" />



5. Once you have done that wait for a successful connection prompt and chat! To quit a chat just type "q" and all messages sent and recieved in this chat will be saved to the DHT so it can be viewed the next time you chat with them.

 <img width="1137" height="566" alt="image" src="https://github.com/user-attachments/assets/da80395f-253f-4691-93ff-8ff1bbdebd22" />


# Offline chats

If you want to send a message to someone who is offline, you can do so by selecting a peer that is offline, it will give you a text prompt that the user is not online and you can send them offline messages which will be written directly to the DHT. To quit just type "q"

<img width="1090" height="225" alt="image" src="https://github.com/user-attachments/assets/f1bf3b1f-c057-45ce-b7e3-4ff0684d2c10" />

