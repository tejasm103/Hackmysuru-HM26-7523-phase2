import os
import sqlite3
import re
import pymysql
from pymysql.cursors import DictCursor
from config import Config

class DatabaseManager:
    def __init__(self):
        self.is_mysql = False
        self.sqlite_path = os.path.join(os.path.dirname(__file__), "adaptivelearn.db")
        self._test_connection()
        self.init_db()

    def _test_connection(self):
        """Attempts to connect to MySQL; if unavailable, activates SQLite Zero-Config Demo Mode."""
        if Config.DB_TYPE.lower() == "mysql":
            try:
                conn = pymysql.connect(
                    host=Config.DB_HOST,
                    port=Config.DB_PORT,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    charset="utf8mb4",
                    connect_timeout=2
                )
                with conn.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4;")
                conn.close()
                self.is_mysql = True
                print(f"[DB] Successfully connected to MySQL server at {Config.DB_HOST}:{Config.DB_PORT}")
                return
            except Exception as e:
                print(f"[DB] Live MySQL server not detected ({e}).")
        
        self.is_mysql = False
        print(f"[DB] Activating Zero-Config Demo Mode using SQLite at: {self.sqlite_path}")

    def get_connection(self):
        if self.is_mysql:
            return pymysql.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                charset="utf8mb4",
                cursorclass=DictCursor,
                autocommit=True
            )
        else:
            conn = sqlite3.connect(self.sqlite_path, timeout=15)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON;")
            return conn

    def _clean_sql_for_sqlite(self, raw_sql):
        """Translates MySQL DDL/DML statements into valid SQLite equivalents."""
        lines = []
        for line in raw_sql.split('\n'):
            if line.strip().startswith('--'):
                continue
            lines.append(line)
        sql = '\n'.join(lines)

        sql = re.sub(r'^\s*CREATE\s+DATABASE\s+[^;]+;', '', sql, flags=re.IGNORECASE | re.MULTILINE)
        sql = re.sub(r'^\s*USE\s+[a-zA-Z0-9_`"\']+\s*;', '', sql, flags=re.IGNORECASE | re.MULTILINE)
        sql = re.sub(r'INT AUTO_INCREMENT PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT', sql, flags=re.IGNORECASE)
        sql = re.sub(r'AUTO_INCREMENT', '', sql, flags=re.IGNORECASE)
        sql = re.sub(r'ENGINE=InnoDB[^;]*', '', sql, flags=re.IGNORECASE)
        sql = re.sub(r'DEFAULT CHARSET=[^;]*', '', sql, flags=re.IGNORECASE)
        sql = re.sub(r'ON UPDATE CURRENT_TIMESTAMP', '', sql, flags=re.IGNORECASE)
        sql = re.sub(r'ENUM\([^)]+\)', 'TEXT', sql, flags=re.IGNORECASE)
        sql = re.sub(r'JSON', 'TEXT', sql, flags=re.IGNORECASE)
        sql = re.sub(r'BOOLEAN', 'INTEGER', sql, flags=re.IGNORECASE)
        sql = re.sub(r'UNIQUE\s+KEY\s+[a-zA-Z0-9_]+\s*\(', 'UNIQUE (', sql, flags=re.IGNORECASE)
        sql = re.sub(r',?\s*INDEX\s+[a-zA-Z0-9_]+\s*\([^)]+\)', '', sql, flags=re.IGNORECASE)
        sql = re.sub(r',\s*\)', ')', sql)
        return sql

    def init_db(self):
        """Initializes tables and seeds if not already populated."""
        schema_file = os.path.join(os.path.dirname(__file__), "schema.sql")
        seed_file = os.path.join(os.path.dirname(__file__), "seed.sql")
        
        if not os.path.exists(schema_file):
            return

        if self.is_mysql:
            conn = self.get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SHOW TABLES LIKE 'users';")
                    if not cursor.fetchone():
                        print("[DB] Initializing MySQL tables from schema.sql...")
                        with open(schema_file, 'r', encoding='utf-8') as f:
                            schema_sql = f.read()
                        for stmt in schema_sql.split(';'):
                            stmt = stmt.strip()
                            if stmt:
                                try:
                                    cursor.execute(stmt)
                                except Exception:
                                    pass
                        
                        if os.path.exists(seed_file):
                            print("[DB] Seeding MySQL database from seed.sql...")
                            with open(seed_file, 'r', encoding='utf-8') as f:
                                seed_sql = f.read()
                            for stmt in seed_sql.split(';'):
                                stmt = stmt.strip()
                                if stmt:
                                    try:
                                        cursor.execute(stmt)
                                    except Exception:
                                        pass
            finally:
                conn.close()
        else:
            conn = self.get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
                if not cursor.fetchone():
                    print("[DB] Initializing SQLite tables from schema.sql...")
                    with open(schema_file, 'r', encoding='utf-8') as f:
                        schema_sql = self._clean_sql_for_sqlite(f.read())
                    for stmt in schema_sql.split(';'):
                        stmt = stmt.strip()
                        if stmt:
                            try:
                                cursor.execute(stmt)
                            except Exception as err:
                                pass
                    conn.commit()

                    if os.path.exists(seed_file):
                        print("[DB] Seeding SQLite database from seed.sql...")
                        with open(seed_file, 'r', encoding='utf-8') as f:
                            seed_sql = self._clean_sql_for_sqlite(f.read())
                        for stmt in seed_sql.split(';'):
                            stmt = stmt.strip()
                            if stmt:
                                try:
                                    if stmt.upper().startswith("INSERT INTO"):
                                        stmt = stmt.replace("INSERT INTO", "INSERT OR REPLACE INTO", 1)
                                    cursor.execute(stmt)
                                except Exception as err:
                                    pass
                        conn.commit()
            finally:
                conn.close()

    def query(self, sql, params=None):
        """Executes a SELECT query and returns a list of dictionaries."""
        conn = self.get_connection()
        try:
            if self.is_mysql:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params or ())
                    return cursor.fetchall()
            else:
                sql_sqlite = sql.replace('%s', '?')
                cursor = conn.cursor()
                cursor.execute(sql_sqlite, params or ())
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_one(self, sql, params=None):
        """Executes a SELECT query and returns a single dictionary or None."""
        results = self.query(sql, params)
        return results[0] if results else None

    def execute(self, sql, params=None):
        """Executes an INSERT/UPDATE/DELETE query and returns lastrowid."""
        conn = self.get_connection()
        try:
            if self.is_mysql:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params or ())
                    last_id = cursor.lastrowid
                return last_id
            else:
                sql_sqlite = sql.replace('%s', '?')
                cursor = conn.cursor()
                cursor.execute(sql_sqlite, params or ())
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()

# Singleton DB instance
db = DatabaseManager()
