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

        try:
            conn = mysql.connector.connect(
                host=settings.MYSQL_HOST,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                database=settings.MYSQL_DATABASE,
                **ssl_args
            )
            print(f"✅ Successfully connected to MySQL database: {settings.MYSQL_DATABASE}")
            return conn
        except mysql.connector.Error as err:
            print(f"❌ Failed to connect to MySQL: {err}")
            raise

    def register_user(self, username, email, password_hash, created_at):
        conn = None
        cursor = None
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Simple check if table exists (console output as requested)
            cursor.execute("SHOW TABLES LIKE 'users'")
            if cursor.fetchone():
                print("✅ Table 'users' verified in database.")
            else:
                print("⚠️ Table 'users' does not exist. Attempting to create it...")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) UNIQUE,
                        email VARCHAR(255),
                        password_hash VARCHAR(255),
                        created_at DATETIME
                    )
                """)
                print("✅ Table 'users' created successfully.")

            query = """
                INSERT INTO users (username, email, password_hash, created_at)
                VALUES (%s, %s, %s, %s)
            """
            values = (username, email, password_hash, created_at)
            cursor.execute(query, values)
            conn.commit()
            print(f"✅ User '{username}' inserted into database.")
            return True, "User registered successfully!"
        except mysql.connector.Error as err:
            print(f"❌ Database operation failed: {err}")
            return False, f"Error: {err}"
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_user_by_username(self, username):
        conn = None
        cursor = None
        try:
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            if user:
                print(f"✅ User '{username}' found in database.")
            else:
                print(f"ℹ️ User '{username}' not found.")
            return user
        except mysql.connector.Error as err:
            print(f"❌ Failed to fetch user: {err}")
            return None
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
