from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from PROJECT.auth.google_auth import setup_logger

class MainWindow(QMainWindow):
    def __init__(self, auth, docs_controller, text_manager, system_interaction, state_store):
        super().__init__()
        self.auth = auth
        self.docs_controller = docs_controller
        self.text_manager = text_manager
        self.system_interaction = system_interaction
        self.state_store = state_store
        self.logger = setup_logger()
        
        # Initialize browser when starting
        self.docs_controller.initialize_browser()
        
        # Setup error handling
        self.setup_error_handling()
        
        self.init_ui()

    def setup_error_handling(self):
        try:
            self.auth.authenticate()
        except Exception as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            # Handle error appropriately

    def init_ui(self):
        self.setWindowTitle("VoiceTyping")
        self.setGeometry(100, 100, 300, 400)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
            QLabel {
                color: #FFFFFF;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("VoiceTyping")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #FF9900; margin-bottom: 15px;")
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
                    background-color: #FF9900;
                    color: #000000;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #FFA500;
                }
                QPushButton:pressed {
                    background-color: #FF8C00;
                }
            """)
            button.setMinimumHeight(50)
            button.clicked.connect(func)
            main_layout.addWidget(button)

        self.status_label = QLabel("Trạng thái: Sẵn sàng")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont('Arial', 10))
        self.status_label.setStyleSheet("color: #AAAAAA; margin-top: 15px;")
        main_layout.addWidget(self.status_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def start_recording(self):
        if not self.state_store.get_state('is_recording'):
            self.state_store.set_state('is_recording', True)
            self.docs_controller.start_voice_typing()
            self.status_label.setText("Trạng thái: Đang ghi âm")
            self.status_label.setStyleSheet("color: #00FF00; margin-top: 15px;")

    def stop_recording(self):
        if self.state_store.get_state('is_recording'):
            self.state_store.set_state('is_recording', False)
            self.docs_controller.stop_voice_typing()
            self.status_label.setText("Trạng thái: Đã dừng ghi âm")
            self.status_label.setStyleSheet("color: #FF0000; margin-top: 15px;")

    def paste_text(self):
        text = self.docs_controller.get_text()
        self.system_interaction.paste_text(text)
        self.status_label.setText("Trạng thái: Đã dán văn bản")
        self.status_label.setStyleSheet("color: #AAAAAA; margin-top: 15px;")