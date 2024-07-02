# add_face.py
import sqlite3
import pickle
import cv2
import face_recognition
from utils.preprocess import preprocess_image

def add_face_to_db(image_path, name):
    aligned_bgr_img, rgb_img = preprocess_image(image_path)
    if rgb_img is None:
        print(f"Error processing image {image_path}")
        return

    face_locations = face_recognition.face_locations(rgb_img)
    face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

    if len(face_encodings) > 0:
        face_encoding = face_encodings[0]
        # Serialize the encoding to store in the database
        face_encoding_blob = pickle.dumps(face_encoding)

        # Connect to the database
        conn = sqlite3.connect('face_recognition.db')
        c = conn.cursor()
        
        # Insert the name and face encoding into the database
        c.execute("INSERT INTO faces (name, encoding) VALUES (?, ?)", (name, face_encoding_blob))
        
        # Commit changes and close the connection
        conn.commit()
        conn.close()
        
        print(f"Added {name} to the database.")
    else:
        print(f"No faces found in {image_path}.")

# Example usage
if __name__ == "__main__":
    image_path = input("Enter the path to the image: ")
    name = input("Enter the name of the person: ")
    add_face_to_db(image_path, name)
