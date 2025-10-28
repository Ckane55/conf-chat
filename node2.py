import asyncio
from kademlia.network import Server
import socket
import time

async def run():
    # Create a node and start listening on port 5678
    node = Server()
    await node.listen(5679)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    # Bootstrap the node by connecting to other known nodes, in this case
    # replace 123.123.123.123 with the IP of another node and optionally
    # give as many ip/port combos as you can for other nodes.
    await node.bootstrap([("10.5.0.2", 5678)])

    # set a value for the key "my-key" on the network
    await node.set("node1", ip)

    await asyncio.sleep(5)

    # get the value associated with "my-key" from the network
    result = await node.get("node1")
    print(result)

asyncio.run(run())