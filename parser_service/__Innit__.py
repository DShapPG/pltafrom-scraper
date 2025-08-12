import asyncio
from connection_pool import create_pool
from cities_parsing import cities_parsing_start

async def main():
    await create_pool()
    await cities_parsing_start()


asyncio.run(main())