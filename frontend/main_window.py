from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon, QTextCursor
from backend.controller import InputController
from backend.recognizer import SpeechRecognizer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoiceTyping")
        self.setFixedSize(400, 200)
        self.setWindowIcon(QIcon("logo.ico"))
        
        # Thiết lập giao diện
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Trạng thái
        status_layout = QHBoxLayout()
        main_layout.addLayout(status_layout)
        self.status_icon = QLabel()
        self.status_icon.setPixmap(QIcon("stop_icon.png").pixmap(QSize(20, 20)))
        status_layout.addWidget(self.status_icon)
        self.status_label = QLabel("Not Activated")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()

        # Hiển thị văn bản
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFixedHeight(60)
        self.text_display.setLineWrapMode(QTextEdit.WidgetWidth)
        main_layout.addWidget(self.text_display)

        # Khởi tạo các thành phần
        self.input_controller = InputController()
        self.recognizer = SpeechRecognizer()
        self.input_controller.ctrl_pressed.connect(self.on_ctrl_pressed)
        self.recognizer.text_recognized.connect(self.update_recognized_text)

    def on_ctrl_pressed(self, pressed):
        if pressed:
            self.start_recognition()
        else:
            self.stop_recognition()

    def start_recognition(self):
        self.status_icon.setPixmap(QIcon("play_icon.png").pixmap(QSize(20, 20)))
        self.status_label.setText("Activated")
        self.recognizer.start_listening()

    def stop_recognition(self):
        self.status_icon.setPixmap(QIcon("stop_icon.png").pixmap(QSize(20, 20)))
        self.status_label.setText("Not Activated")
        self.recognizer.stop_listening()

    def update_recognized_text(self, text):
        current_text = self.text_display.toPlainText()
        lines = current_text.split('\n')
        if len(lines) >= 2:
            lines = lines[-1:]
        lines.append(text)
        new_text = '\n'.join(lines[-2:])
        self.text_display.setText(new_text)
        cursor = self.text_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.text_display.setTextCursor(cursor)
        self.text_display.ensureCursorVisible()

if __name__ == "__main__":
    app = QApplication([])
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    app.exec_()
