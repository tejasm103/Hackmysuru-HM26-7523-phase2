import re
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "database", "adaptivelearn.db")
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

with open("database/schema.sql", "r", encoding="utf-8") as f:
    raw_sql = f.read()

def clean_for_sqlite(sql):
    lines = []
    for line in sql.split('\n'):
        line_clean = re.sub(r'--.*$', '', line)
        lines.append(line_clean)
    sql = '\n'.join(lines)

    sql = re.sub(r'CREATE DATABASE[^;]+;', '', sql, flags=re.IGNORECASE)
    sql = re.sub(r'USE [^;]+;', '', sql, flags=re.IGNORECASE)
    sql = re.sub(r'INT AUTO_INCREMENT PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT', sql, flags=re.IGNORECASE)
    sql = re.sub(r'AUTO_INCREMENT', '', sql, flags=re.IGNORECASE)
    sql = re.sub(r'ENGINE=InnoDB[^;]*', '', sql, flags=re.IGNORECASE)
    sql = re.sub(r'DEFAULT CHARSET=[^;]*', '', sql, flags=re.IGNORECASE)
    sql = re.sub(r'ON UPDATE CURRENT_TIMESTAMP', '', sql, flags=re.IGNORECASE)
    sql = re.sub(r'ENUM\([^)]+\)', 'TEXT', sql, flags=re.IGNORECASE)
    sql = re.sub(r'JSON', 'TEXT', sql, flags=re.IGNORECASE)
    sql = re.sub(r'BOOLEAN', 'INTEGER', sql, flags=re.IGNORECASE)
    # Replace MySQL 'UNIQUE KEY uq_name (col1, col2)' with standard 'UNIQUE (col1, col2)'
    sql = re.sub(r'UNIQUE\s+KEY\s+[a-zA-Z0-9_]+\s*\(', 'UNIQUE (', sql, flags=re.IGNORECASE)
    # Remove INDEX clauses inside CREATE TABLE (e.g. INDEX idx_user_email (email),)
    sql = re.sub(r',?\s*INDEX\s+[a-zA-Z0-9_]+\s*\([^)]+\)', '', sql, flags=re.IGNORECASE)
    # Fix trailing commas before closing paren
    sql = re.sub(r',\s*\)', ')', sql)
    return sql

cleaned = clean_for_sqlite(raw_sql)
errors = []
success = 0
for i, stmt in enumerate(cleaned.split(';')):
    stmt = stmt.strip()
    if stmt:
        try:
            cursor.execute(stmt)
            success += 1
        except Exception as e:
            errors.append((i, str(e), stmt[:80]))

print(f"Success: {success}, Errors: {len(errors)}")
for idx, err, snippet in errors:
    print(f"[{idx}] {err} -> {snippet}")

conn.commit()
tables = [row[0] for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print(f"Tables now in DB: {len(tables)}")
conn.close()
