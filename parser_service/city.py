from connection_pool import get_connection
from psycopg2 import errors


async def insert_or_update_city(cities):
    conn = await get_connection()
    try:
        await conn.executemany("""
            INSERT INTO cities (name, url, slug, path, region_id, olx_id)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (url) DO UPDATE SET
                name = EXCLUDED.name,
                slug = EXCLUDED.slug,
                path = EXCLUDED.path,
                olx_id = EXCLUDED.olx_id,
                region_id = EXCLUDED.region_id;
        """, cities)
        return True  # или количество записей (не asyncpg), либо просто True

    except Exception as e:
        print(f"Reason: {e}")
        return False

    finally:
        await conn.close()



def delete_city(city_id):
    with get_connection() as connection:
        with connection.cursor() as cur:
            cur.execute("""
                DELETE FROM cities WHERE id = %s;
            """, (city_id,))
            connection.commit()