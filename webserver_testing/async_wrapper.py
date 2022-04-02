import asyncio
import threading
from bybit_ws_factory import BybitWsManagerFactory


class AsyncConsumer:
    def __init__(self, consumer):
        """Wrap a synchronous kafka consumer in this class to make it asynchronous"""
        self.waiter = asyncio.Future()
        self.consumer = consumer
    
    def __repr__(self):
        return f"AsyncConsumer: topic=bybit"

    def publish(self, value):
        waiter, self.waiter = self.waiter, asyncio.Future()
        waiter.set_result((value, self.waiter))
    
    async def run_consumer(self, stop):
        while not (stop.is_set() or shutdown_all.is_set()):
            data = await asyncio.to_thread(self.consumer.get_msg)
            if data:
                print("Publishing")
                self.publish(data)
                print("Published")

    async def get_msg(self):
        waiter = self.waiter
        while True:
            value, waiter = await waiter
            print("Waited")
            yield value

    __aiter__ = get_msg


# {topic: Event}
threads = {}
shutdown_all = threading.Event()

async def get_consumer(topic):
    consumer = AsyncConsumer(BybitWsManagerFactory().get_ws_manager(topic))
    event = threading.Event()
    asyncio.create_task(consumer.run_consumer(event))
    threads[topic] = event
    print(f"{topic} consumer started")
    return consumer

def shutdown_topic(topic):
    threads[topic].set()
    timeout = 1
    print(f"topic {topic} didn't terminate within {timeout} seconds")
    del threads[topic]
    print(f"{topic} consumer stopped")

def shutdown():
    shutdown_all.set()


async def main():
    consumer = await get_consumer("BTCUSD")
    async for msg in consumer:
        print(msg)

if __name__ == "__main__":
    asyncio.run(main())