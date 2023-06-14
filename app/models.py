import shortuuid
from database import create_connection

def create_short_link(original_url):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            existing_link = get_link_by_url(original_url)
            if existing_link is not None:
                return existing_link
            else:
                short_code = shortuuid.uuid()[:8]
                if not original_url.startswith("http://") and not original_url.startswith("https://"):
                    # Agregar "http://" como prefijo a la URL original
                    original_url = "http://" + original_url
                sql = "INSERT INTO urls (link, short_url) VALUES (%s, %s)"
                cursor.execute(sql, (original_url, short_code))
                connection.commit()
                return short_code
    finally:
        connection.close()

def get_link_by_url(original_url):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT short_url FROM urls WHERE link = %s"
            cursor.execute(sql, (original_url,))
            result = cursor.fetchone()
            if result:
                short_url = result["short_url"]
                return short_url
            else:
                return None
    finally:
        connection.close()