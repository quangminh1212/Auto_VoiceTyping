from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QTextEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QTextCursor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoiceTyping")
        self.setGeometry(100, 100, 400, 500)  # Tăng kích thước cửa sổ
        self.setStyleSheet("""
            QMainWindow {
                background-color: #333333;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 18px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #4FC3F7;
                color: #000000;
                border: none;
                padding: 10px;
                margin: 10px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #81D4FA;
            }
            QPushButton:pressed {
                background-color: #29B6F6;
            }
            QTextEdit {
                background-color: #FFFFFF;
                color: #000000;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.status_label = QLabel("Trạng thái: Chưa kích hoạt")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setPlaceholderText("Văn bản đã nhận diện sẽ hiển thị ở đây...")
        layout.addWidget(self.text_display)

        self.start_button = QPushButton("Bắt đầu nhận diện")
        self.start_button.clicked.connect(self.start_recognition)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Dừng nhận diện")
        self.stop_button.clicked.connect(self.stop_recognition)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

    def start_recognition(self):
        self.status_label.setText("Trạng thái: Đang nhận diện...")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_recognition(self):
        self.status_label.setText("Trạng thái: Đã dừng")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_recognized_text(self, text):
        cursor = self.text_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text + " ")
        self.text_display.setTextCursor(cursor)
        self.text_display.ensureCursorVisible()

if __name__ == "__main__":
    app = QApplication([])
    app.setFont(QFont("Roboto", 12))  # Sử dụng font Roboto
    window = MainWindow()
    window.show()
    app.exec_()