from PyQt6.QtWidgets import (QMainWindow, QPushButton, 
                           QVBoxLayout, QWidget, QLabel)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, docs_controller):
        super().__init__()
        self.docs_controller = docs_controller
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Voice Typing")
        self.setMinimumSize(400, 300)
        
        # Widget chính
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        
        # Các nút điều khiển
        start_btn = QPushButton("Bắt đầu ghi âm")
        stop_btn = QPushButton("Dừng ghi âm")
        get_text_btn = QPushButton("Lấy văn bản")
        
        # Kết nối sự kiện
        start_btn.clicked.connect(self.docs_controller.start_voice_typing)
        stop_btn.clicked.connect(self.docs_controller.stop_voice_typing)
        get_text_btn.clicked.connect(self.docs_controller.get_text)
        
        # Thêm vào layout
        layout.addWidget(QLabel("Voice Typing Tool"))
        layout.addWidget(start_btn)
        layout.addWidget(stop_btn)
        layout.addWidget(get_text_btn)
        layout.addStretch()
        
        main_widget.setLayout(layout)