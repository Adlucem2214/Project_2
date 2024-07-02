import sys
from PyQt5 import QtWidgets, QtGui
from tkinter import filedialog, messagebox
from recognition.add_face import add_face_to_db
from recognition.face_recognition import recognize_faces
import threading

class FaceRecognitionApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Face Recognition System')
        self.setGeometry(100, 100, 800, 400)
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QtWidgets.QVBoxLayout()

        title_label = QtWidgets.QLabel("Face Recognition System")
        title_label.setFont(QtGui.QFont("Helvetica", 16, QtGui.QFont.Bold))
        title_label.setStyleSheet("color: #333333;")
        # title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        form_layout = QtWidgets.QFormLayout()
        
        self.name_entry = QtWidgets.QLineEdit()
        form_layout.addRow('Name:', self.name_entry)

        self.path_entry = QtWidgets.QLineEdit()
        self.browse_button = QtWidgets.QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_image)
        path_layout = QtWidgets.QHBoxLayout()
        path_layout.addWidget(self.path_entry)
        path_layout.addWidget(self.browse_button)
        form_layout.addRow('Image Path:', path_layout)

        layout.addLayout(form_layout)

        button_layout = QtWidgets.QHBoxLayout()

        self.add_face_button = QtWidgets.QPushButton('Add Face')
        self.add_face_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.add_face_button.clicked.connect(self.add_face)
        button_layout.addWidget(self.add_face_button)

        self.start_recognition_button = QtWidgets.QPushButton('Start Recognition')
        self.start_recognition_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.start_recognition_button.clicked.connect(self.start_recognition)
        button_layout.addWidget(self.start_recognition_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def browse_image(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select an Image", "", "Image Files (*.jpg *.jpeg *.png *.webp)")
        if file_path:
            self.path_entry.setText(file_path)

    def add_face(self):
        file_path = self.path_entry.text()
        name = self.name_entry.text()
        if file_path and name:
            add_face_to_db(file_path, name)
            QtWidgets.QMessageBox.information(self, "Success", f"Face for {name} added successfully!")
        else:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please provide both name and image.")

    def start_recognition(self):
        threading.Thread(target=recognize_faces).start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = FaceRecognitionApp()
    ex.show()
    sys.exit(app.exec_())
