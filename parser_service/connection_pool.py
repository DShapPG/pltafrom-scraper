import asyncpg

pool = None

async def create_pool():
    global pool
    pool = await asyncpg.create_pool(
        host="localhost",
        database="OLX",
        user="dshap",
        password="987987gg",
        port=5432,
        min_size=1,
        max_size=10
    )

async def get_connection():
    return await pool.acquire()

async def release_connection(conn):
    await pool.release(conn)
