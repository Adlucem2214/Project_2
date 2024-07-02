import pickle
import sqlite3


def load_known_faces():
    # Connect to the database
    conn = sqlite3.connect('face_recognition.db')
    c = conn.cursor()
    
    # Fetch all rows from the faces table
    c.execute("SELECT name, encoding FROM faces")
    known_face_encodings = []
    known_face_names = []
    
    for row in c.fetchall():
        name, encoding_blob = row
        encoding = pickle.loads(encoding_blob)
        known_face_encodings.append(encoding)
        known_face_names.append(name)
    
    # Close the connection
    conn.close()
    
    return known_face_encodings, known_face_names
