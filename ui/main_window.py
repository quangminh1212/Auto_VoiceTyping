"""
Voice Typing Application
Author: Bach Gia
Email: wuangming12@gmail.com
Version: 1.0.0
"""

from PyQt6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QWidget, 
                           QMessageBox, QLabel, QProgressBar, QTextEdit, QApplication,
                           QHBoxLayout, QComboBox, QSpinBox, QCheckBox)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QTextCursor, QIcon
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.audio_service import AudioService
from controllers.docs_controller import DocsController
from utils.text_manager import TextManager
from utils.system_interaction import SystemInteraction
from utils.state_store import StateStore

class MainWindow(QMainWindow):
    def __init__(self, auth, docs_controller, text_manager, system_interaction, state_store):
        super().__init__()
        self.auth = auth
        self.docs_controller = docs_controller
        self.text_manager = text_manager
        self.system_interaction = system_interaction
        self.state_store = state_store

        self.recording_timer = QTimer()
        self.recording_timer.timeout.connect(self.update_timer)
        self.recording_seconds = 0
        
        self.text_update_timer = QTimer()
        self.text_update_timer.timeout.connect(self.update_text_display)
        self.text_update_timer.setInterval(100)
        
        self.last_text = ""
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()

        # Header với logo và thông tin
        header_layout = QHBoxLayout()
        logo_label = QLabel('Voice Typing')
        logo_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            padding: 10px;
        """)
        header_layout.addWidget(logo_label)
        
        author_label = QLabel('by Bach Gia (wuangming12@gmail.com)')
        author_label.setStyleSheet('color: #666; padding: 5px;')
        header_layout.addWidget(author_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Text Display Area
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setMinimumHeight(250)
        self.text_display.setFont(QFont('Arial', 14))
        self.text_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                padding: 15px;
                border: 2px solid #4CAF50;
                border-radius: 10px;
            }
        """)
        self.text_display.setPlaceholderText("Văn bản sẽ hiển thị ở đây...")
        main_layout.addWidget(self.text_display)

        # Control Panel
        control_layout = QHBoxLayout()
        
        # Microphone Selection
        self.mic_combo = QComboBox()
        self.mic_combo.addItems(self.system_interaction.get_audio_devices())
        self.mic_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                min-width: 150px;
            }
        """)
        control_layout.addWidget(self.mic_combo)

        # Recording Controls
        button_style = """
            QPushButton {
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """

        self.start_button = QPushButton('🎤 Bắt đầu ghi âm (Ctrl+R)')
        self.start_button.setStyleSheet(button_style + "background-color: #4CAF50;")
        self.start_button.clicked.connect(self.start_recording)
        control_layout.addWidget(self.start_button)

        self.stop_button = QPushButton('⏹ Dừng ghi âm (Ctrl+S)')
        self.stop_button.setStyleSheet(button_style + "background-color: #f44336;")
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)
        control_layout.addWidget(self.stop_button)

        self.clear_button = QPushButton('🗑 Xóa văn bản')
        self.clear_button.setStyleSheet(button_style + "background-color: #2196F3;")
        self.clear_button.clicked.connect(self.clear_text)
        control_layout.addWidget(self.clear_button)

        main_layout.addLayout(control_layout)

        # Settings Panel
        settings_layout = QHBoxLayout()
        
        # Auto-save settings
        self.auto_save = QCheckBox('Tự động lưu')
        self.auto_save.setStyleSheet('padding: 5px;')
        settings_layout.addWidget(self.auto_save)
        
        # Language selection
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['Tiếng Việt', 'English'])
        self.lang_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)
        settings_layout.addWidget(self.lang_combo)

        main_layout.addLayout(settings_layout)

        # Status Bar
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel('Trạng thái: Sẵn sàng')
        self.status_label.setStyleSheet("""
            padding: 5px;
            color: #666;
            font-weight: bold;
        """)
        status_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        self.progress_bar.hide()
        status_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(status_layout)

        main_widget.setLayout(main_layout)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Voice Typing')
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
        """)

    def load_settings(self):
        # Load saved settings
        geometry = self.state_store.get_state('window_geometry')
        if geometry:
            self.setGeometry(*geometry)
            
        last_device = self.state_store.get_state('last_used_device')
        if last_device:
            index = self.mic_combo.findText(last_device)
            if index >= 0:
                self.mic_combo.setCurrentIndex(index)

    def clear_text(self):
        reply = QMessageBox.question(self, 'Xác nhận', 
                                   'Bạn có chắc muốn xóa toàn bộ văn bản?',
                                   QMessageBox.StandardButton.Yes | 
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.text_display.clear()
            self.text_manager.set_text("")
            self.last_text = ""

    def update_text_display(self):
        try:
            current_text = self.docs_controller.get_text()
            if current_text and current_text != self.last_text:
                self.text_display.setText(current_text)
                cursor = self.text_display.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.End)
                self.text_display.setTextCursor(cursor)
                self.last_text = current_text
                
                # Auto-save if enabled
                if self.auto_save.isChecked():
                    self.text_manager.set_text(current_text)
                
        except Exception as e:
            print(f"Lỗi cập nhật text: {str(e)}")

    def start_recording(self):
        try:
            print("\n=== BẮT ĐẦU GHI ÂM ===")
            self.state_store.set_state('is_recording', True)
            
            # Update UI
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.mic_combo.setEnabled(False)
            self.status_label.setText("Đang ghi âm: 00:00")
            self.progress_bar.show()
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            
            # Start recording
            self.docs_controller.start_voice_typing()
            self.recording_seconds = 0
            self.recording_timer.start(1000)
            self.text_update_timer.start()
            
        except Exception as e:
            self.handle_error("Không thể bắt đầu ghi âm", e)

    def stop_recording(self):
        try:
            print("\n=== DỪNG GHI ÂM ===")
            self.state_store.set_state('is_recording', False)
            
            # Update UI
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.mic_combo.setEnabled(True)
            self.status_label.setText("Trạng thái: Sẵn sàng")
            self.progress_bar.hide()
            
            # Stop recording
            text = self.docs_controller.stop_voice_typing()
            self.recording_timer.stop()
            self.text_update_timer.stop()
            
            if text and text.strip():
                print(f"Văn bản đã ghi: [{text}]")
                
        except Exception as e:
            self.handle_error("Không thể dừng ghi âm", e)

    def handle_error(self, message, error):
        print(f"Lỗi: {message} - {str(error)}")
        self.status_label.setText(f"Lỗi: {message}")
        QMessageBox.critical(self, "Lỗi", f"{message}: {str(error)}")
        
        # Reset state
        self.state_store.set_state('is_recording', False)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.mic_combo.setEnabled(True)
        self.progress_bar.hide()

    def update_timer(self):
        self.recording_seconds += 1
        minutes = self.recording_seconds // 60
        seconds = self.recording_seconds % 60
        self.status_label.setText(f"Đang ghi âm: {minutes:02d}:{seconds:02d}")
        
        # Update progress bar
        if self.recording_seconds % 2 == 0:
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(50)
        else:
            self.progress_bar.setRange(0, 0)

    def closeEvent(self, event):
        # Save settings before closing
        self.state_store.set_state('window_geometry', 
                                 (self.x(), self.y(), self.width(), self.height()))
        self.state_store.set_state('last_used_device', 
                                 self.mic_combo.currentText())
        event.accept()

def main():
    print("\n=== VOICE TYPING APP ===")
    print("Author: Bach Gia")
    print("Email: wuangming12@gmail.com")
    print("Version: 1.0.0")
    print("\nĐang khởi tạo...")
    
    app = QApplication(sys.argv)
    
    # Khởi tạo các dependencies
    auth = None
    docs_controller = DocsController()
    text_manager = TextManager()
    system_interaction = SystemInteraction()
    state_store = StateStore()
    
    window = MainWindow(auth, docs_controller, text_manager, system_interaction, state_store)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()