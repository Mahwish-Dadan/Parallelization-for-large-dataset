# db_handler.py

import sqlite3
from config import DB_FILE
from datetime import datetime

def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            worker_id TEXT,
            rows_processed INTEGER,
            total_sales REAL,
            min_price REAL,
            max_price REAL,
            avg_price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_result(result):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO results (worker_id, rows_processed, total_sales, min_price, max_price, avg_price)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        result['worker_id'],
        result['rows_processed'],
        result['total_sales'],
        result['min_price'],
        result['max_price'],
        result['avg_price']
    ))
    conn.commit()
    conn.close()

def aggregate_results():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT
            SUM(rows_processed),
            SUM(total_sales),
            MIN(min_price),
            MAX(max_price),
            AVG(avg_price)
        FROM results
    ''')
    result = c.fetchone()
    conn.close()
    return result
