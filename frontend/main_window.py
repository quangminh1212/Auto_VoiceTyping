from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QTextCursor, QPalette, QColor, QFont
from backend.controller import InputController
from backend.recognizer import SpeechRecognizer
import logging

# Cấu hình logging
logger = logging.getLogger("MainWindow")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoiceTyping")
        self.setFixedSize(300, 150)  # Tăng kích thước để chứa thông báo lỗi
        self.setWindowIcon(QIcon("logo.ico"))
        
        logger.info("Khởi tạo MainWindow")
        self.setup_dark_theme()
        self.setup_ui()
        
        self.input_controller = InputController()
        self.recognizer = SpeechRecognizer()
        
        # Kết nối tín hiệu
        self.input_controller.ctrl_pressed.connect(self.on_ctrl_pressed)
        self.input_controller.text_typed.connect(self.on_text_typed)
        self.recognizer.text_recognized.connect(self.on_text_recognized)
        self.recognizer.error_occurred.connect(self.show_error)
        
        logger.info("MainWindow đã khởi tạo xong")

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
        
        # Thêm label hiển thị trạng thái
        self.status_label = QLabel("Sẵn sàng")
        self.status_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 12px;
                padding: 5px;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

    def toggle_recognition(self):
        if self.toggle_button.text() == "Start":
            self.start_recognition()
        else:
            self.stop_recognition()

    def on_ctrl_pressed(self, pressed):
        if pressed:
            logger.info("Phím Ctrl được nhấn, bắt đầu nhận dạng")
            self.start_recognition()
        else:
            logger.info("Phím Ctrl được nhả, dừng nhận dạng")
            self.stop_recognition()
    
    def on_text_recognized(self, text):
        logger.info(f"Nhận dạng văn bản: '{text}'")
        self.status_label.setText(f"Đang nhập: {text[:20]}...")
        self.input_controller.type_text(text)
    
    def on_text_typed(self, success, text):
        if success:
            self.status_label.setText(f"Đã nhập: {text[:20]}...")
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #4CAF50;
                    font-size: 12px;
                    padding: 5px;
                }
            """)
            # Tự động đổi về trạng thái bình thường sau 3 giây
            QTimer.singleShot(3000, self.reset_status_label)
        else:
            error_msg = f"Lỗi khi nhập: {text[:20]}..."
            logger.error(error_msg)
            self.show_error(error_msg)
    
    def reset_status_label(self):
        if self.recognizer.is_listening:
            self.status_label.setText("Đang lắng nghe...")
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #4CAF50;
                    font-size: 12px;
                    padding: 5px;
                }
            """)
        else:
            self.status_label.setText("Sẵn sàng")
            self.status_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 12px;
                    padding: 5px;
                }
            """)
            
    def show_error(self, error_message):
        logger.error(f"Lỗi: {error_message}")
        self.status_label.setText(error_message)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #f44336;
                font-size: 12px;
                padding: 5px;
            }
        """)
        # Dừng nhận dạng nếu có lỗi nghiêm trọng
        if "FFmpeg" in error_message or "microphone" in error_message:
            self.stop_recognition()

    def start_recognition(self):
        logger.info("Bắt đầu nhận dạng giọng nói")
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
        self.status_label.setText("Đang lắng nghe...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 12px;
                padding: 5px;
            }
        """)
        self.recognizer.start_listening()

    def stop_recognition(self):
        logger.info("Dừng nhận dạng giọng nói")
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
        self.status_label.setText("Sẵn sàng")
        self.status_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 12px;
                padding: 5px;
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