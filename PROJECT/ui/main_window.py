from PyQt6.QtWidgets import (QMainWindow, QPushButton, 
                           QVBoxLayout, QWidget, QLabel, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextCursor

class MainWindow(QMainWindow):
    def __init__(self, docs_controller):
        super().__init__()
        self.docs_controller = docs_controller
        # Kết nối signal với slot
        self.docs_controller.text_received.connect(self.update_text)
        self.setup_ui()
        
    def update_text(self, new_text):
        """Cập nhật text mới vào text area"""
        cursor = self.text_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(new_text + " ")
        self.text_area.setTextCursor(cursor)
        self.text_area.ensureCursorVisible()
        
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
        
        # Thêm status label
        self.status_label = QLabel("Trạng thái: Chưa ghi âm")
        self.status_label.setStyleSheet("color: gray;")
        
        # Kết nối sự kiện
        start_btn.clicked.connect(self.start_recording)
        stop_btn.clicked.connect(self.stop_recording)
        get_text_btn.clicked.connect(self.get_text)
        
        # Thêm vào layout
        layout.addWidget(title)
        layout.addWidget(self.text_area)
        layout.addWidget(start_btn)
        layout.addWidget(stop_btn)
        layout.addWidget(get_text_btn)
        layout.addWidget(self.status_label)
        
        main_widget.setLayout(layout)
        
    def start_recording(self):
        if self.docs_controller.start_voice_typing():
            self.status_label.setText("Trạng thái: Đang ghi âm...")
            self.status_label.setStyleSheet("color: green;")
            
    def stop_recording(self):
        if self.docs_controller.stop_voice_typing():
            self.status_label.setText("Trạng thái: Đã dừng ghi âm")
            self.status_label.setStyleSheet("color: red;")
            
    def get_text(self):
        text = self.docs_controller.get_text()
        if text:
            self.text_area.setText(text)
            self.status_label.setText("Trạng thái: Đã copy văn bản")
        else:
            self.status_label.setText("Trạng thái: Chưa có văn bản mới")