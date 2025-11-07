import asyncio
IP = "127.0.0.1"

async def handle_peer(reader, writer):
    peer = writer.get_extra_info("peername")
    print(f"SERVER [CONNECTED] {peer} connected.")
    try:
        while True:
            data = await reader.readline()
            if not data:
                print(f"[DISCONNECTED] {peer}")
                break
            print(data.decode().strip())
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def start_server(port):
    server = await asyncio.start_server(handle_peer, IP, port)
    print(f"[LISTENING] on port {port}")
    async with server:
        await server.serve_forever()

async def connect_to_peer(port, username):
    while True:
        try:
            reader, writer = await asyncio.open_connection(IP, port)
            print(f"INITIAL CONNECTION [CONNECTED to {port}]")
            break
        except ConnectionRefusedError:
            print("[FAILED] retrying in 2s...")
            await asyncio.sleep(2)

    # Task to read messages from peer we connected to
    async def read_messages():
        try:
            while True:
                data = await reader.readline()
                if not data:
                    print("[PEER DISCONNECTED]")
                    break
                print(data.decode().strip())
        except Exception as e:
            print(f"[RECV ERROR] {e}")

    asyncio.create_task(read_messages())

    # Sending messages (input)
    loop = asyncio.get_event_loop()
    try:
        while True:
            msg = await loop.run_in_executor(None, input, f"{username}: ")
            writer.write(f"{username}: {msg}\n".encode())
            await writer.drain()
    except Exception as e:
        print(f"[SEND ERROR] {e}")
        writer.close()
        await writer.wait_closed()

async def start_chat(your_port, your_username, peer_port):
    # Start server in background
    asyncio.create_task(start_server(your_port))

    # Connect to peer after server starts
  
    await connect_to_peer(peer_port, your_username)


