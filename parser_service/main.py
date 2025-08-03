from psycopg2 import connect
from db import connection
from psycopg2 import errors


def insert_or_update_category(title, slug, url, path, parent_id=None):
    try:
        with connection.cursor() as cur:
            cur.execute("""
                INSERT INTO categories (title, slug, url, path, parent_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (slug) DO UPDATE SET
                    title = EXCLUDED.title,
                    url = EXCLUDED.url,
                    path = EXCLUDED.path,
                    parent_id = EXCLUDED.parent_id,
                    updated_at = NOW()
                RETURNING id;
            """, (title, slug, url, path, parent_id))
            new_id = cur.fetchone()[0]
            connection.commit()
            return new_id
    except errors.UniqueViolation:
        connection.rollback()
        with connection.cursor() as cur:
            cur.execute("""
                INSERT INTO categories (title, slug, url, path, parent_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (url) DO UPDATE SET
                    title = EXCLUDED.title,
                    slug = EXCLUDED.slug,
                    path = EXCLUDED.path,
                    parent_id = EXCLUDED.parent_id,
                    updated_at = NOW()
                RETURNING id;
            """, (title, slug, url, path, parent_id))
            new_id = cur.fetchone()[0]
            connection.commit()
            return new_id

def delete_category(category_id):
    with connection.cursor() as cur:
        cur.execute("""
            DELETE FROM categories WHERE id = %s;
        """, (category_id,))
        connection.commit()

    
# new_id = insert_category(conn, "Electronics", "electronics", "https://example.com/electronics")
# print(f"Inserted category with id {new_id}")

# Удаляем категорию
# delete_category(conn, 1)
# print(f"Deleted category with id ")

