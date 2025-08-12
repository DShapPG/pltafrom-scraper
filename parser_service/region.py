from connection_pool import get_connection
from psycopg2 import errors

def insert_or_update_region(name, url, slug, path, olx_id):
    try:
        with get_connection() as connection:
            with connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO regions (name, url, slug, path, olx_id)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO UPDATE SET
                        name = EXCLUDED.name,
                        slug = EXCLUDED.slug,
                        path = EXCLUDED.path,
                        olx_id = EXCLUDED.olx_id
                    RETURNING id;
                """, (name, url, slug, path, olx_id))
                new_id = cur.fetchone()[0]
                connection.commit()
                return new_id

    except errors.UniqueViolation:
        connection.rollback()


async def delete_region(region_id):
    connection = await get_connection()
    try:
        async with connection.transaction():
            await connection.execute("""
                DELETE FROM regions WHERE id = $1;
            """, region_id)
    finally:
        await connection.close()


async def get_region_id_by_olx_id(region_olx_id):
    connection = await get_connection()
    try:
        result = await connection.fetchrow("""
            SELECT id FROM regions WHERE olx_id = $1;
        """, region_olx_id)
        return result['id'] if result else None
    finally:
        await connection.close()

async def get_all_regions_olx_ids():
    connection = await get_connection()
    try:
        results = await connection.fetch("SELECT olx_id FROM regions;")
        return [record['olx_id'] for record in results]
    finally:
        await connection.close()