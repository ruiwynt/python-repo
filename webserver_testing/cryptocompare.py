import asyncio
import json
import websockets

total_delay = 0
n_processed = 0

def average_delay(data):
	global total_delay
	global n_processed
	if 'DELAYNS' in data.keys():
		total_delay += data['DELAYNS']
		n_processed += 1
	else:
		print(json.dumps(data, indent=1))

async def cryptocompare():
    # this is where you paste your api key
    api_key = "8c2446452f504a03f59b196dd10c6a06dbaa9882c428b30481f524e740bb2d35"
    url = "wss://streamer.cryptocompare.com/v2?api_key=" + api_key
    async with websockets.connect(url) as websocket:
        await websocket.send(json.dumps({
            "action": "SubAdd",
            "subs": ["8~Binance~BTC~USDT"],
        }))
        while True:
            try:
                data = await websocket.recv()
            except websockets.ConnectionClosed:
                break
            try:
                data = json.loads(data)
                average_delay(data)
                if n_processed > 0:
                    print(f"N_PROCESSED: {n_processed}\nAVG_DELAY: {int(total_delay/n_processed/10**(6))} MILLISECONDS\n")
            except ValueError:
                print(data)

asyncio.get_event_loop().run_until_complete(cryptocompare())