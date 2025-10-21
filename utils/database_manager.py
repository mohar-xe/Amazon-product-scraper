import sqlite3
from datetime import datetime
import logging


class DatabaseManager:
    def __init__(self, db_path='data.db'):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            logging.info(f"Database connection opened to {self.db_path}")
            return self
        except sqlite3.Error as e:
            logging.error(f"Database connection error: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed.")

    def setup_database(self):
        if not self.conn:
            raise ConnectionError("Database not connected. Use within a 'with' block.")

        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                rating TEXT,
                image_url TEXT,
                source_url TEXT NOT NULL,
                scraped_at TIMESTAMP NOT NULL
            )
        ''')
        self.conn.commit()
        logging.info("Database table 'products' is set up.")

    def insert_data(self, data, source_url):
        if not self.conn:
            raise ConnectionError("Database not connected.")
        if not data:
            logging.warning(f"No data provided to insert for {source_url}.")
            return

        cursor = self.conn.cursor()
        now = datetime.now()

        records_to_insert = [
            (
                item['name'],
                item['price'],
                item.get('rating', 'N/A'),
                item.get('image_url', 'N/A'),
                source_url,
                now
            ) for item in data
        ]

        cursor.executemany('''
            INSERT INTO products (name, price, rating, image_url, source_url, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', records_to_insert)

        self.conn.commit()
        logging.info(f"Inserted {len(records_to_insert)} records from {source_url}.")
