from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QTextCursor, QPalette, QColor
from backend.controller import InputController
from backend.recognizer import SpeechRecognizer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoiceTyping")
        self.setFixedSize(300, 100)  # Giảm chiều cao xuống
        self.setWindowIcon(QIcon("logo.ico"))
        
        self.setup_dark_theme()
        self.setup_ui()
        
        self.input_controller = InputController()
        self.recognizer = SpeechRecognizer()
        self.input_controller.alt_pressed.connect(self.on_alt_pressed)
        self.recognizer.text_recognized.connect(self.input_controller.type_text)

    def setup_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(45, 45, 45))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        self.setPalette(palette)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.toggle_button = QPushButton("Start")
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_recognition)
        layout.addWidget(self.toggle_button)

    def toggle_recognition(self):
        if self.toggle_button.text() == "Start":
            self.start_recognition()
        else:
            self.stop_recognition()

    def on_alt_pressed(self, pressed):
        if pressed:
            self.start_recognition()
        else:
            self.stop_recognition()

    def start_recognition(self):
        self.toggle_button.setText("Stop")
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.recognizer.start_listening()

    def stop_recognition(self):
        self.toggle_button.setText("Start")
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.recognizer.stop_listening()


    def toggle_display(self):
        self.is_display_expanded = not self.is_display_expanded
        if self.is_display_expanded:
            self.text_display.setFixedHeight(300)
            self.toggle_display_button.setText("Thu gọn")
        else:
            self.text_display.setFixedHeight(100)
            self.toggle_display_button.setText("Mở rộng")
        self.adjustSize()

if __name__ == "__main__":
    app = QApplication([])
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    app.exec_()