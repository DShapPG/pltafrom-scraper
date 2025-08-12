from connection_pool import get_connection

def init_db():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    slug TEXT,
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
                    category_id INT NULL REFERENCES categories(id) ON DELETE SET NULL,
                    url TEXT UNIQUE,
                    price TEXT,
                    description TEXT,
                    district_id INT NULL,
                    city_id INT NULL,
                    region_id INT NULL,
                    views INT NULL,
                    photo_urls TEXT[],
                    parameters JSONB

                );
            """)

            cursor.execute("""
               CREATE TABLE IF NOT EXISTS regions(
                   id SERIAL PRIMARY KEY,
                   name TEXT,
                   created_at TIMESTAMP DEFAULT NOW(),
                   updated_at TIMESTAMP DEFAULT NOW(),
                   url TEXT UNIQUE,
                   slug TEXT,
                   path TEXT,
                   olx_id INT NULL UNIQUE
                   );
               """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cities (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    url TEXT UNIQUE,
                    slug TEXT,
                    path TEXT,
                    region_id INT NULL REFERENCES regions(id) ON DELETE SET NULL,
                    olx_id INT NULL UNIQUE
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS districts (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    url TEXT UNIQUE,
                    slug TEXT,
                    path TEXT,
                    city_id INT NULL REFERENCES cities(id) ON DELETE SET NULL,
                    olx_id INT NULL UNIQUE
                );
            """)






        connection.commit()



# init_db()
