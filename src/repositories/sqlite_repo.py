import sqlite3
from src.config.settings import settings

class SQLiteRepository:
    def __init__(self):
        self.db_file = settings.SQLITE_DB_FILE
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS engagement_metrics5 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                xAxis TEXT,
                yAxis REAL
            )
        ''')
        conn.commit()
        conn.close()

    def save_engagement(self, x_values, y_values):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        for x, y in zip(x_values, y_values):
            cursor.execute(
                "INSERT INTO engagement_metrics5 (xAxis, yAxis) VALUES (?, ?)",
                (x, y)
            )
        conn.commit()
        conn.close()

    def get_all_engagement(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM engagement_metrics5")
        data = cursor.fetchall()
        conn.close()
        return data
