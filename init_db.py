import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Turfs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS turfs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    location TEXT,
    price_per_slot INTEGER
    slots TEXT
)
""")

# Bookings table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    turf_id INTEGER,
    date TEXT,
    slot TEXT,
    amount INTEGER,
    status TEXT
)
""")

# Income table
cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT,
    source TEXT,
    amount INTEGER
)
""")

# Expenses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT,
    category TEXT,
    amount INTEGER
)
""")

conn.commit()
conn.close()

print("Database initialized successfully!")
