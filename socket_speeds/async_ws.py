import asyncio
import websockets
import time
import json


queue = asyncio.Queue()
start_time = None

async def count_queue():
    while True:
        print(f"Messages Received: {queue.qsize()}")
        print(f"Messages p/s: {queue.qsize()/(time.time()-start_time)}")
        await asyncio.sleep(1)

async def receive_messages(ws):
    async for msg in ws:
        await queue.put(msg)

async def receive_kraken()

async def main():
    global start_time
    url = 'wss://ws-feed.pro.coinbase.com'

    async with websockets.connect(url) as ws:
        start_time = time.time()
        await ws.send(json.dumps({
            "type": "subscribe",
            "channels": [{"name": "full", "product_ids": ["BTC-USD"]}]}
        ))

        asyncio.create_task(count_queue())
        await receive_messages(ws)


if __name__ == "__main__":
    asyncio.run(main())