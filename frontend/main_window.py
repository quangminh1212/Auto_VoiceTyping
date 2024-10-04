from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoiceTyping")
        self.setGeometry(100, 100, 300, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.status_label = QLabel("Trạng thái: Chưa kích hoạt")
        layout.addWidget(self.status_label)

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
        # Thêm logic để bắt đầu nhận diện giọng nói ở đây

    def stop_recognition(self):
        self.status_label.setText("Trạng thái: Đã dừng")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        # Thêm logic để dừng nhận diện giọng nói ở đây

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
