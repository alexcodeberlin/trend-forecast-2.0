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

    def register_user(self, username, email, password_hash, created_at):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO users (username, email, password_hash, created_at)
                VALUES (%s, %s, %s, %s)
            """
            values = (username, email, password_hash, created_at)
            cursor.execute(query, values)
            conn.commit()
            return True, "User registered successfully!"
        except mysql.connector.Error as err:
            return False, f"Error: {err}"
        finally:
            cursor.close()
            conn.close()
