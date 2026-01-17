import sqlite3

conn = sqlite3.connect("data/exams.db")
conn.execute("PRAGMA journal_mode=WAL;")
print("WAL mode enabled")

conn.close()
