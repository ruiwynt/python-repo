import asyncio
import time
from webbrowser import BackgroundBrowser


counter = 0
def get_resource():
    global counter
    print(f"producer: Sleeping for 1 second, then returning {counter}")
    time.sleep(1)
    counter += 1
    print(f"producer: returning {counter}")
    return counter

async def produce(aioqueue):
    while True:
        print(f"producer: calling get_resource")
        msg = await asyncio.to_thread(get_resource)
        print(f"producer: putting into queue")
        await aioqueue.put(msg)
        print(f"producer: put {msg} into queue")

async def consume(aioqueue):
    while True:
        print("consumer: waiting for aioqueue")
        msg = await aioqueue.get()
        print(f"consumer: {msg}")

async def bg_process():
    while True:
        # print("background: ye")
        await asyncio.sleep(0.5)

async def main():
    aioqueue = asyncio.Queue()
    asyncio.create_task(produce(aioqueue))
    await asyncio.gather(
        consume(aioqueue),
        bg_process()
    )

if __name__ == "__main__":
    asyncio.run(main())