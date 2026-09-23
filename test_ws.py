import asyncio
import websockets
import json

async def test():
    try:
        async with websockets.connect("wss://laser-tag-laser-tag-server.onrender.com") as ws:
            print("Connected!")
            await ws.send(json.dumps({"type": "ADMIN_JOIN"}))
            response = await ws.recv()
            print(f"Received: {response}")
    except Exception as e:
        print(f"Failed: {e}")

asyncio.run(test())
