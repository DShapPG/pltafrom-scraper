from connection_pool import get_connection


def insert_or_update_listing():
    pass
def delete_listing():
    pass

def is_url_not_in_listings(url):
    with get_connection() as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT 1 FROM listings WHERE url = %s LIMIT 1;", (url,))
            return cur.fetchone() is None