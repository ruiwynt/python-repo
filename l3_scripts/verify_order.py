import asyncio
import websockets
import json # For the json.dumps function

endpoint = "ws://194.233.73.248:30205/"
topic = 'bybit'
feed = 'normalised'

current_quote_no = -1
n_incorrect = 0
total = 0

async def connect():
    global current_quote_no, n_incorrect, total
    print("Connecting")
    async with websockets.connect(endpoint) as websocket:
        print("Connected")
        request = {'op': 'subscribe', 'exchange': topic, 'feed': feed}
        request_json = json.dumps(request).encode('utf-8')
        await websocket.send(request_json) # Sending message to service
        print("Subscribed")

        # Printing out data
        async for message in websocket:
            msg_dict = json.loads(message)
            if 'quote_no' in msg_dict.keys():
                if current_quote_no == -1:
                    current_quote_no = msg_dict['quote_no']
                else:
                    if msg_dict['quote_no'] != current_quote_no + 1:
                        print(f"error rate: {n_incorrect/total * 100}")
                        n_incorrect += 1
                current_quote_no = msg_dict['quote_no']
                # print(f"Received quote no: {current_quote_no}")
                total += 1

async def main():
    await connect()

if __name__ == "__main__":
    asyncio.run(main())
