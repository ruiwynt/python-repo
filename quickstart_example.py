import asyncio
import websockets
import json # For the json.dumps function

endpoint = "ws://194.233.73.248:30205/"

async def connect():
	async with websockets.connect(endpoint) as websocket:
		print("Connected")

		# Subscribing to Okex raw feed
		request = {'op': 'subscribe', 'topic': 'okex'}
		request_json = json.dumps(request).encode('utf-8')
		await websocket.send(request_json)
		print("Subscribed")

		# Printing out data
		async for message in websocket:
                    print(message)

if __name__ == "__main__":
	asyncio.run(connect())
