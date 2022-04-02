import asyncio
import websockets
import aioconsole
import json

connections = set()

async def recv(ws):
    async for msg in ws:
        print(f"\n<<< {msg}\n>>> ", end = "")

async def send():
    while True:
        await asyncio.sleep(1)
        websockets.broadcast(connections, "Hello!")

async def poll(ws):
    await ws.wait_closed()
    connections.remove(ws)

async def handler(ws):
    print("Connection Accepted")
    connections.add(ws)
    recv_task = asyncio.create_task(recv(ws))
    poll_task = asyncio.create_task(poll(ws))
    done, pending = await asyncio.wait(
        [recv_task, poll_task],
        return_when = asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()

async def start_server():
    async with websockets.serve(handler, "localhost", 37000):
        print("Server Running")
        await asyncio.Future()

async def debug():
    while True:
        print(f"\ndebug: {connections}")
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(
        start_server(),
        debug(),
        send()
    )

if __name__ == "__main__":
    asyncio.run(main(), debug=True)