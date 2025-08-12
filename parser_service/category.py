from connection_pool import get_connection
from psycopg2 import errors


def insert_or_update_category(title, slug, url, path, parent_id=None):
    try:
        with get_connection() as connection:
            with connection.cursor() as cur:
                cur.execute("""
                INSERT INTO categories (title, slug, url, path, parent_id)
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT (url) DO
                UPDATE SET
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
    except errors.UniqueViolation:
        connection.rollback()


def delete_category(category_id):
    with get_connection() as connection:
        with connection.cursor() as cur:
            cur.execute("""
                DELETE FROM categories WHERE id = %s;
            """, (category_id,))
            connection.commit()

def get_category_id_by_slug(slug):
    with get_connection() as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT id FROM categories WHERE slug = %s", (slug,))
            result = cur.fetchone()
            return result[0] if result else None


def get_category_id_by_url(url):
    with get_connection() as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT id FROM categories WHERE url = %s", (url,))
            result = cur.fetchone()
            return result[0] if result else None

def get_categories_urls():
    with get_connection() as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT url FROM categories WHERE parent_id IS NOT NULL;")
            return [row[0] for row in cur.fetchall()]



