from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self, auth, docs_controller, text_manager, system_interaction, state_store):
        super().__init__()
        self.auth = auth
        self.docs_controller = docs_controller
        self.text_manager = text_manager
        self.system_interaction = system_interaction
        self.state_store = state_store

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("VoiceTyping")
        self.setGeometry(100, 100, 300, 400)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1A1A1A;
            }
            QLabel {
                color: #CCCCCC;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        title_label = QLabel("VoiceTyping")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #FFA500; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        buttons = [
            ("Bắt đầu ghi âm", self.start_recording, "🎙️"),
            ("Dừng ghi âm", self.stop_recording, "⏹️"),
            ("Dán văn bản", self.paste_text, "📋")
        ]

        for text, func, icon in buttons:
            button = QPushButton(f"{icon} {text}")
            button.setFont(QFont('Arial', 12))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #333333;
                    color: #CCCCCC;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #444444;
                }
                QPushButton:pressed {
                    background-color: #555555;
                }
            """)
            button.setMinimumHeight(50)
            button.clicked.connect(func)
            main_layout.addWidget(button)

        self.status_label = QLabel("Trạng thái: Sẵn sàng")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont('Arial', 10))
        self.status_label.setStyleSheet("color: #999999; margin-top: 10px;")
        main_layout.addWidget(self.status_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def start_recording(self):
        if not self.state_store.get_state('is_recording'):
            self.state_store.set_state('is_recording', True)
            self.docs_controller.start_voice_typing()
            QMessageBox.information(self, "Thông báo", "Bắt đầu ghi âm")

    def stop_recording(self):
        if self.state_store.get_state('is_recording'):
            self.state_store.set_state('is_recording', False)
            self.docs_controller.stop_voice_typing()
            QMessageBox.information(self, "Thông báo", "Dừng ghi âm")

    def paste_text(self):
        text = self.docs_controller.get_text()
        self.system_interaction.paste_text(text)
        QMessageBox.information(self, "Thông báo", "Đã dán văn bản")