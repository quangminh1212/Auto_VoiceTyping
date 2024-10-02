from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtCore import QTimer

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
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        start_button = QPushButton("Bắt đầu ghi âm")
        start_button.clicked.connect(self.start_recording)
        layout.addWidget(start_button)

        stop_button = QPushButton("Dừng ghi âm")
        stop_button.clicked.connect(self.stop_recording)
        layout.addWidget(stop_button)

        paste_button = QPushButton("Dán văn bản")
        paste_button.clicked.connect(self.paste_text)
        layout.addWidget(paste_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
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