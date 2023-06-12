import pymysql

def create_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='urls',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def check_connection():
    connection_chk = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection_chk

def create_database():
    connection = check_connection()
    try:
        with connection.cursor() as cursor:
            sql = "CREATE DATABASE IF NOT EXISTS urls"
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()

def create_table():
    connection = check_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("USE urls")
            sql = """
            CREATE TABLE IF NOT EXISTS urls (
                id INT AUTO_INCREMENT PRIMARY KEY,
                link VARCHAR(1024),
                short_url VARCHAR(8) UNIQUE,
                hits INT DEFAULT 0
            )
            """
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()

def check_database():
    connection = check_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SHOW DATABASES LIKE 'urls'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if not result:
                create_database()
            create_table()
    finally:
        connection.close()