import sqlite3
import json
import logging
import requests
from datetime import datetime


# manage a local sqlite to store sensor data when the api is unreachable
class SensorBuffer:
    def __init__(self, db_path="sensor_buffer.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._initialize_db()

    # create the buffer table if it doesn't exist
    def _initialize_db(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS buffer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            data TEXT
        )
        """)
        self.conn.commit()

    def store_locally(self, data):
        self.cursor.execute(
            "INSERT INTO buffer (timestamp, data) VALUES (?, ?)",
            (datetime.now().isoformat(), json.dumps(data)),
        )
        self.conn.commit()

    def resend_buffered_data(self, api_url):
        self.cursor.execute("SELECT id, data FROM buffer ORDER BY id")
        rows = self.cursor.fetchall()

        for row in rows:
            record_id, data_json = row
            data = json.loads(data_json)

            try:
                response = requests.post(api_url, json=data, timeout=5)

                if response.status_code == 200:
                    self.cursor.execute("DELETE FROM buffer WHERE id=?", (record_id,))
                    self.conn.commit()
                    logging.info(f"[BUFFER SENT] {data}")

            except Exception:
                logging.error("[ERROR] Failed to resend buffered data")
                break

    def close(self):
        self.conn.close()
