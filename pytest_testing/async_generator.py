import asyncio


async def generate(x):
    await asyncio.sleep(3)
    return x