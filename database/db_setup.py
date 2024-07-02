import sqlite3


conn = sqlite3.connect('face_recognition.db')


c = conn.cursor()


c.execute('''
CREATE TABLE IF NOT EXISTS faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    encoding BLOB NOT NULL
)
''')


conn.commit()
conn.close()

print("Database setup complete.")
