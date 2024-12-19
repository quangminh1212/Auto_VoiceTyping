from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from utils.logger import setup_logger

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
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2C3E50, stop:1 #3498DB);
            }
            QLabel {
                color: #ECF0F1;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E74C3C, stop:1 #C0392B);
                color: white;
                border: none;
                padding: 15px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #C0392B, stop:1 #E74C3C);
            }
            QPushButton:pressed {
                background: #C0392B;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title_label = QLabel("VoiceTyping")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Segoe UI', 32, QFont.Weight.Bold))
        title_label.setStyleSheet("""
            color: #ECF0F1;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px #000000;
        """)
        main_layout.addWidget(title_label)

        # Buttons
        buttons = [
            ("🎙️ Bắt đầu ghi âm", self.start_recording),
            ("⏹️ Dừng ghi âm", self.stop_recording),
            ("📋 Dán văn bản", self.paste_text)
        ]

        for text, func in buttons:
            button = QPushButton(text)
            button.setFont(QFont('Segoe UI', 12))
            button.setMinimumHeight(60)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(func)
            main_layout.addWidget(button)

        # Status
        self.status_label = QLabel("Trạng thái: Sẵn sàng")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont('Segoe UI', 12))
        self.status_label.setStyleSheet("""
            color: #2ECC71;
            background-color: rgba(0, 0, 0, 0.2);
            padding: 10px;
            border-radius: 5px;
            margin-top: 20px;
        """)
        main_layout.addWidget(self.status_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def start_recording(self):
        if not self.state_store.get_state('is_recording'):
            self.state_store.set_state('is_recording', True)
            self.docs_controller.start_voice_typing()
            self.status_label.setText("Trạng thái: Đang ghi âm")
            self.status_label.setStyleSheet("""
                color: #E74C3C;
                background-color: rgba(0, 0, 0, 0.2);
                padding: 10px;
                border-radius: 5px;
            """)

    def stop_recording(self):
        if self.state_store.get_state('is_recording'):
            self.state_store.set_state('is_recording', False)
            self.docs_controller.stop_voice_typing()
            self.status_label.setText("Trạng thái: Đã dừng ghi âm")
            self.status_label.setStyleSheet("""
                color: #F1C40F;
                background-color: rgba(0, 0, 0, 0.2);
                padding: 10px;
                border-radius: 5px;
            """)

    def paste_text(self):
        text = self.docs_controller.get_text()
        self.system_interaction.paste_text(text)
        self.status_label.setText("Trạng thái: Đã dán văn bản")
        self.status_label.setStyleSheet("""
            color: #2ECC71;
            background-color: rgba(0, 0, 0, 0.2);
            padding: 10px;
            border-radius: 5px;
        """)