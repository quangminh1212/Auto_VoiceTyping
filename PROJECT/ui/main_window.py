from PyQt6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, 
                           QWidget, QLabel, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

class MainWindow(QMainWindow):
    def __init__(self, docs_controller):
        super().__init__()
        self.docs_controller = docs_controller
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Voice Typing Tool")
        self.setMinimumSize(500, 400)
        
        # Widget chính
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        
        # Tiêu đề
        title = QLabel("VOICE TYPING TOOL")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        
        # Text area để hiển thị văn bản
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Văn bản sẽ hiển thị ở đây...")
        self.text_area.setReadOnly(True)
        
        # Các nút điều khiển
        start_btn = QPushButton("Bắt đầu ghi âm")
        start_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        
        stop_btn = QPushButton("Dừng ghi âm")
        stop_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px;")
        
        get_text_btn = QPushButton("Lấy văn bản")
        get_text_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        
        help_btn = QPushButton("Hướng dẫn")
        help_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 10px;")
        
        # Kết nối sự kiện
        start_btn.clicked.connect(self.start_recording)
        stop_btn.clicked.connect(self.stop_recording)
        get_text_btn.clicked.connect(self.get_text)
        help_btn.clicked.connect(self.docs_controller.show_instructions)
        
        # Thêm vào layout
        layout.addWidget(title)
        layout.addWidget(self.text_area)
        layout.addWidget(start_btn)
        layout.addWidget(stop_btn)
        layout.addWidget(get_text_btn)
        layout.addWidget(help_btn)
        
        main_widget.setLayout(layout)
        
    def start_recording(self):
        if self.docs_controller.start_voice_typing():
            self.statusBar().showMessage("Đang ghi âm...")
            
    def stop_recording(self):
        if self.docs_controller.stop_voice_typing():
            self.statusBar().showMessage("Đã dừng ghi âm")
            
    def get_text(self):
        text = self.docs_controller.get_text()
        if text:
            self.text_area.setText(text)
            self.statusBar().showMessage("Đã lấy văn bản thành công")
        else:
            self.statusBar().showMessage("Chưa có văn bản mới")