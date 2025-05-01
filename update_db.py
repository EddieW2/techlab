import sqlite3

conn = sqlite3.connect('techlab.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE purchases ADD COLUMN returned BOOLEAN DEFAULT 0")
    print("✅ Column 'returned' added successfully.")
except sqlite3.OperationalError as e:
    print("⚠️ Column may already exist or error occurred:", e)

conn.commit()
conn.close()
