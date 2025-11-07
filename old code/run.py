import asyncio



async def handle_client(reader, writer):
    while True:
        data = await reader.readline()
        if not data:
            break
        print(f"[recv] {data.decode().strip()}")

async def run_server(your_port):
    server = await asyncio.start_server(handle_client, "127.0.0.1", your_port)
    print(f"[LISTENING on {your_port}]")
    async with server:
        await server.serve_forever()

async def run_client(peer_port):
    reader = writer = None
    while True:
        try:
            if not reader:
                reader, writer = await asyncio.open_connection("127.0.0.1", peer_port)
                print(f"[CONNECTED to {peer_port}]")
                asyncio.create_task(read_server(reader))
            msg = await asyncio.get_event_loop().run_in_executor(None, input)
            writer.write((msg + "\n").encode())
            await writer.drain()
        except ConnectionRefusedError:
            print("[WAITING FOR PEER]")
            await asyncio.sleep(2)

async def read_server(reader):
    while True:
        data = await reader.readline()
        if not data:
            print("[DISCONNECTED]")
            return
        print(f"[peer] {data.decode().strip()}")

async def start_chat(your_port,your_username, peer_port):
    asyncio.create_task(run_server(your_port))
    await run_client(peer_port)

asyncio.run(start_chat(5002, "Caden", 5001))

