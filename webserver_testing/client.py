import websockets
import asyncio
import aioconsole

async def recv(ws):
    async for msg in ws:
        print(f"\n<<< {msg}\n>>> ", end = "")

async def send(ws):
    while True:
        print(">>> ", end = "")
        message = await aioconsole.ainput()
        if message == "/exit":
            break
        await ws.send(message)

async def main():
    async with websockets.connect("ws://localhost:37000/") as ws:
        print("Connected")
        try:
            recv_task = asyncio.create_task(recv(ws))
            send_task = asyncio.create_task(send(ws))
            done, pending = await asyncio.wait(
                [recv_task, send_task],
                return_when = asyncio.FIRST_COMPLETED
            )
            for task in pending:
                task.cancel()
        except websockets.ConnectionClosed:
            print("ConnectionClosed exeption raised")

if __name__ == "__main__":
    asyncio.run(main(), debug=True)