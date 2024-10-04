from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoiceTyping")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 18px;
                margin-bottom: 20px;
            }
            QPushButton {
                background-color: #CCCCCC;
                color: #000000;
                border: none;
                padding: 10px;
                margin: 10px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #4FC3F7;
            }
            QPushButton:pressed {
                background-color: #0288D1;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.status_label = QLabel("Trạng thái: Chưa kích hoạt")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.start_button = QPushButton("Bắt đầu nhận diện")
        self.start_button.setIcon(QIcon("path/to/mic_icon.png"))  # Thêm biểu tượng microphone
        self.start_button.clicked.connect(self.start_recognition)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Dừng nhận diện")
        self.stop_button.setIcon(QIcon("path/to/stop_icon.png"))  # Thêm biểu tượng dừng
        self.stop_button.clicked.connect(self.stop_recognition)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

    def start_recognition(self):
        self.status_label.setText("Trạng thái: Đang nhận diện...")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        # Thêm logic để bắt đầu nhận diện giọng nói ở đây

    def stop_recognition(self):
        self.status_label.setText("Trạng thái: Đã dừng")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        # Thêm logic để dừng nhận diện giọng nói ở đây

if __name__ == "__main__":
    app = QApplication([])
    app.setFont(QFont("Roboto", 12))  # Sử dụng font Roboto
    window = MainWindow()
    window.show()
    app.exec_()
