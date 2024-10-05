from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QLabel, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QTextCursor  # Thêm QTextCursor vào đây

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoiceTyping")
        self.setFixedSize(400, 200)  # Tăng chiều cao để chứa text display lớn hơn
        self.setWindowIcon(QIcon("logo.png"))  # Add your logo file here
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4A4A4A;
                color: #FFFFFF;
                border: none;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5A5A5A;
            }
            QPushButton:pressed {
                background-color: #6A6A6A;
            }
            QTextEdit {
                background-color: #3A3A3A;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        status_layout = QHBoxLayout()
        main_layout.addLayout(status_layout)

        self.status_icon = QLabel()
        self.status_icon.setPixmap(QIcon("stop_icon.png").pixmap(QSize(20, 20)))
        status_layout.addWidget(self.status_icon)

        self.status_label = QLabel("Not Activated")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        self.start_button = QPushButton("Start")
        self.start_button.setIcon(QIcon("play_icon.png"))
        self.start_button.setIconSize(QSize(20, 20))
        self.start_button.clicked.connect(self.start_recognition)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setIcon(QIcon("stop_icon.png"))
        self.stop_button.setIconSize(QSize(20, 20))
        self.stop_button.clicked.connect(self.stop_recognition)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)

        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFixedHeight(60)  # Tăng chiều cao để hiển thị 2 dòng
        self.text_display.setLineWrapMode(QTextEdit.WidgetWidth)
        main_layout.addWidget(self.text_display)

    def start_recognition(self):
        self.status_label.setText("Listening...")
        self.status_icon.setPixmap(QIcon("play_icon.png").pixmap(QSize(20, 20)))
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_recognition(self):
        self.status_label.setText("Stopped")
        self.status_icon.setPixmap(QIcon("stop_icon.png").pixmap(QSize(20, 20)))
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_recognized_text(self, text):
        current_text = self.text_display.toPlainText()
        lines = current_text.split('\n')
        if len(lines) >= 2:
            lines = lines[-1:]  # Giữ lại dòng cuối cùng
        lines.append(text)
        new_text = '\n'.join(lines[-2:])  # Chỉ giữ 2 dòng cuối cùng
        self.text_display.setText(new_text)
        self.text_display.moveCursor(QTextCursor.End)  # Di chuyển con trỏ đến cuối

if __name__ == "__main__":
    app = QApplication([])
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    app.exec_()
