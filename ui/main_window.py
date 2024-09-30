from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, auth, docs_controller, text_manager, system_interaction, state_store):
        super().__init__()
        self.auth = auth
        self.docs_controller = docs_controller
        self.text_manager = text_manager
        self.system_interaction = system_interaction
        self.state_store = state_store
        
        self.setWindowTitle("VoiceTyping")
        self.setGeometry(100, 100, 300, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout()
        
        self.login_button = QPushButton("Đăng nhập Google")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)
        
        self.start_button = QPushButton("Bắt đầu ghi âm")
        self.start_button.clicked.connect(self.start_recording)
        layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Dừng ghi âm")
        self.stop_button.clicked.connect(self.stop_recording)
        layout.addWidget(self.stop_button)
        
        self.paste_button = QPushButton("Dán văn bản")
        self.paste_button.clicked.connect(self.paste_text)
        layout.addWidget(self.paste_button)
        
        self.central_widget.setLayout(layout)
    
    def login(self):
        self.auth.authenticate()
    
    def start_recording(self):
        self.docs_controller.start_voice_typing()
    
    def stop_recording(self):
        self.docs_controller.stop_voice_typing()
    
    def paste_text(self):
        text = self.text_manager.get_text()
        self.system_interaction.paste_text(text)