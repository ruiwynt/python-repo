import asyncio 

from async_generator import generate

class GeneratorConsumer:
    async def calculate(self):
        return await generate(3) + 1