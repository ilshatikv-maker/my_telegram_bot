import sqlite3
import json
from datetime import datetime


class Database:
    def __init__(self, db_name="travelmate.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Пользователи
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            full_name TEXT,
            created_at TIMESTAMP
        )
        ''')

        # Поездки
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            destination TEXT,
            start_date DATE,
            end_date DATE,
            budget REAL,
            notes TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        # Достопримечательности
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS places (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            country TEXT,
            city TEXT,
            category TEXT,
            description TEXT,
            price_range TEXT,
            rating REAL
        )
        ''')

        self.conn.commit()

    def add_user(self, telegram_id, username, full_name):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR IGNORE INTO users (telegram_id, username, full_name, created_at)
        VALUES (?, ?, ?, ?)
        ''', (telegram_id, username, full_name, datetime.now()))
        self.conn.commit()
        return cursor.lastrowid

    def add_trip(self, user_id, title, destination, start_date=None, end_date=None, budget=0, notes=""):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO trips (user_id, title, destination, start_date, end_date, budget, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, title, destination, start_date, end_date, budget, notes, datetime.now()))
        self.conn.commit()
        return cursor.lastrowid

    def get_user_trips(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM trips WHERE user_id = ? AND is_active = 1 ORDER BY created_at DESC', (user_id,))
        return cursor.fetchall()

    def close(self):
        self.conn.close()