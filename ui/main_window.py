from PyQt6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QWidget, 
                           QMessageBox, QLabel, QProgressBar, QTextEdit)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QTextCursor

class MainWindow(QMainWindow):
    def __init__(self, auth, docs_controller, text_manager, system_interaction, state_store):
        super().__init__()
        self.auth = auth
        self.docs_controller = docs_controller
        self.text_manager = text_manager
        self.system_interaction = system_interaction
        self.state_store = state_store

        # Timer cho ghi âm
        self.recording_timer = QTimer()
        self.recording_timer.timeout.connect(self.update_timer)
        self.recording_seconds = 0
        
        # Timer cho cập nhật text
        self.text_update_timer = QTimer()
        self.text_update_timer.timeout.connect(self.update_text_display)
        self.text_update_timer.setInterval(100)  # Cập nhật mỗi 100ms
        
        self.init_ui()
        self.last_text = ""  # Lưu text cuối cùng để so sánh

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # Text display area
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setMinimumHeight(200)
        self.text_display.setFont(QFont('Arial', 14))  # Font size lớn hơn
        self.text_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)
        self.text_display.setPlaceholderText("Văn bản sẽ hiển thị ở đây...")
        layout.addWidget(self.text_display)

        # Các nút điều khiển
        button_style = """
            QPushButton {
                padding: 10px;
                font-size: 12px;
                border-radius: 5px;
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

        self.start_button = QPushButton('Bắt đầu ghi âm (Ctrl+R)')
        self.start_button.setStyleSheet(button_style)
        self.start_button.clicked.connect(self.start_recording)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Dừng ghi âm (Ctrl+S)')
        self.stop_button.setStyleSheet(button_style)
        self.stop_button.clicked.connect(self.stop_recording)
        layout.addWidget(self.stop_button)

        # Status area
        self.status_label = QLabel('Trạng thái: Sẵn sàng')
        self.status_label.setStyleSheet('padding: 5px; color: #666;')
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        main_widget.setLayout(layout)
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Voice Typing')

    def update_text_display(self):
        """Cập nhật text display theo realtime"""
        try:
            current_text = self.docs_controller.get_text()
            if current_text and current_text != self.last_text:
                print(f"Đã nhận dạng được: [{current_text}]")
                self.text_display.setText(current_text)
                # Di chuyển con trỏ xuống cuối
                cursor = self.text_display.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.End)
                self.text_display.setTextCursor(cursor)
                self.last_text = current_text
                
        except Exception as e:
            print(f"Lỗi cập nhật text display: {str(e)}")

    def start_recording(self):
        try:
            print("\n=== BẮT ĐẦU GHI ÂM ===")
            self.state_store.set_state('is_recording', True)
            self.docs_controller.start_voice_typing()
            
            # Reset và start các timer
            self.recording_seconds = 0
            self.recording_timer.start(1000)
            self.text_update_timer.start()
            
            # Cập nhật UI
            self.status_label.setText("Đang ghi âm: 00:00")
            self.progress_bar.show()
            self.text_display.clear()
            self.text_display.setPlaceholderText("Đang lắng nghe...")
            self.last_text = ""
            
        except Exception as e:
            print(f"Lỗi khi bắt đầu ghi âm: {str(e)}")
            self.state_store.set_state('is_recording', False)
            QMessageBox.critical(self, "Lỗi", f"Không thể bắt đầu ghi âm: {str(e)}")

    def stop_recording(self):
        try:
            print("\n=== DỪNG GHI ÂM ===")
            self.state_store.set_state('is_recording', False)
            text = self.docs_controller.stop_voice_typing()
            
            # Dừng các timer
            self.recording_timer.stop()
            self.text_update_timer.stop()
            
            # Cập nhật UI
            self.status_label.setText("Trạng thái: Sẵn sàng")
            self.progress_bar.hide()
            
            if text and text.strip():
                print(f"Văn bản cuối cùng: [{text}]")
                self.text_display.setText(text)
            
        except Exception as e:
            print(f"Lỗi khi dừng ghi âm: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể dừng ghi âm: {str(e)}")

    def update_timer(self):
        self.recording_seconds += 1
        minutes = self.recording_seconds // 60
        seconds = self.recording_seconds % 60
        self.status_label.setText(f"Đang ghi âm: {minutes:02d}:{seconds:02d}")