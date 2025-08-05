from psycopg2 import connect
def init_db():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    slug TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    parent_id INT NULL,
                    path TEXT,
                    url TEXT UNIQUE                    
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS listings (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    category_id INT NULL,
                    url TEXT UNIQUE,
                    price TEXT,
                    description TEXT,
                    district_id INT NULL,
                    city_id INT NULL,
                    state_id INT NULL,
                    views INT NULL,
                    photo_urls JSONB,
                    parameters TEXT[]
                    
                );
            """)

        connection.commit()

def get_connection():
    return connect(
        host="ep-tiny-shadow-a2wj1iaj-pooler.eu-central-1.aws.neon.tech",
        dbname="neondb",
        user="neondb_owner",
        password="npg_1lH4OUBpZdck"
    )

connection = get_connection()