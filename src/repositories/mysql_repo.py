import mysql.connector
from src.config.settings import settings

class MySQLRepository:
    def connect(self):
        ssl_args = {}
        if settings.MYSQL_SSL_CA:
            ssl_args["ssl_ca"] = settings.MYSQL_SSL_CA
        if settings.MYSQL_SSL_CERT:
            ssl_args["ssl_cert"] = settings.MYSQL_SSL_CERT
        if settings.MYSQL_SSL_KEY:
            ssl_args["ssl_key"] = settings.MYSQL_SSL_KEY

        return mysql.connector.connect(
            host=settings.MYSQL_HOST,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DATABASE,
            **ssl_args
        )

    def setup_table(self):
        conn = None
        cursor = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            query = """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at DATETIME NOT NULL
                )
            """
            cursor.execute(query)
            conn.commit()
            print("✅ MySQL users table ready.")
        except mysql.connector.Error as err:
            print(f"❌ MySQL setup failed: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def register_user(self, username, email, password_hash, created_at):
        conn = None
        cursor = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            query = """
                INSERT INTO users (username, email, password_hash, created_at)
                VALUES (%s, %s, %s, %s)
            """
            values = (username, email, password_hash, created_at)
            cursor.execute(query, values)
            conn.commit()
            return True, "User registered successfully!"
        except mysql.connector.Error as err:
            return False, f"Database Error: {err}"
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_user_by_username(self, username):
        conn = None
        cursor = None
        try:
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"❌ MySQL fetch error: {err}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
