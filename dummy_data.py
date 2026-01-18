import sqlite3
from datetime import date, timedelta

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# -------------------------------
# CLEAR OLD DATA
# -------------------------------
cursor.execute("DELETE FROM bookings")
cursor.execute("DELETE FROM income")
cursor.execute("DELETE FROM expenses")
cursor.execute("DELETE FROM turfs")

# -------------------------------
# INSERT TURF
# -------------------------------
cursor.execute("""
INSERT INTO turfs (name, location, price_per_slot)
VALUES ('GreenField Turf', 'Chennai', 1200)
""")

turf_id = cursor.lastrowid

# -------------------------------
# HELPER FUNCTION
# -------------------------------
def generate_bookings(start_date, days, peak_slots, dull_slots):
    current_date = start_date
    for _ in range(days):
        for slot in peak_slots:
            cursor.execute("""
                INSERT INTO bookings (turf_id, date, slot, amount, status)
                VALUES (?, ?, ?, ?, 'Confirmed')
            """, (turf_id, current_date.isoformat(), slot, 1200))

        for slot in dull_slots:
            cursor.execute("""
                INSERT INTO bookings (turf_id, date, slot, amount, status)
                VALUES (?, ?, ?, ?, 'Confirmed')
            """, (turf_id, current_date.isoformat(), slot, 1200))

        current_date += timedelta(days=1)

# -------------------------------
# DECEMBER (MODERATE DEMAND)
# -------------------------------
generate_bookings(
    start_date=date(2025, 12, 1),
    days=12,  # increased from 10
    peak_slots=["6AM-7AM", "7AM-8AM", "6PM-7PM", "7PM-8PM"],
    dull_slots=["2PM-3PM"]
)

# -------------------------------
# JANUARY (GOOD BUT NOT EXTREME)
# -------------------------------
generate_bookings(
    start_date=date(2026, 1, 1),
    days=14,  # slightly reduced
    peak_slots=[
        "6AM-7AM", "7AM-8AM",
        "6PM-7PM", "7PM-8PM", "8PM-9PM"
    ],
    dull_slots=["2PM-3PM"]
)

# -------------------------------
# EXTRA INCOME
# -------------------------------
cursor.execute("""
INSERT INTO income (month, source, amount)
VALUES
('December', 'Snacks', 5000),
('January', 'Snacks', 8000)
""")

# -------------------------------
# EXPENSES (REALISTIC & STABLE)
# -------------------------------
cursor.execute("""
INSERT INTO expenses (month, category, amount)
VALUES
('December', 'Staff', 18000),
('December', 'Electricity', 16000),
('December', 'Maintenance', 16000),

('January', 'Staff', 20000),
('January', 'Electricity', 18000),
('January', 'Maintenance', 22000)
""")

conn.commit()
conn.close()

print("✅ Dummy data updated with realistic profit difference!")
