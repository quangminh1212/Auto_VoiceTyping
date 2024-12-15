from PyQt6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QWidget, 
                           QMessageBox, QLabel, QShortcut, QProgressBar)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QKeySequence

class MainWindow(QMainWindow):
    def __init__(self, auth, docs_controller, text_manager, system_interaction, state_store):
        super().__init__()
        self.auth = auth
        self.docs_controller = docs_controller
        self.text_manager = text_manager
        self.system_interaction = system_interaction
        self.state_store = state_store

        # Khởi tạo timer cho việc ghi âm
        self.recording_timer = QTimer()
        self.recording_timer.timeout.connect(self.update_timer)
        self.recording_seconds = 0

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("VoiceTyping")
        self.setGeometry(100, 100, 300, 450)  # Tăng chiều cao để chứa thêm các widget
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1A1A1A;
            }
            QLabel {
                color: #CCCCCC;
            }
            QProgressBar {
                border: 2px solid #444444;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #FFA500;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Tiêu đề
        title_label = QLabel("VoiceTyping")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #FFA500; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        # Thanh tiến trình
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)

        buttons = [
            ("Bắt đầu ghi âm (Ctrl+R)", self.start_recording, "🎙️"),
            ("Dừng ghi âm (Ctrl+S)", self.stop_recording, "⏹️"),
            ("Dán văn bản (Ctrl+V)", self.paste_text, "📋"),
            ("Xem trước văn bản", self.preview_text, "👀")
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

        # Status label
        self.status_label = QLabel("Trạng thái: Sẵn sàng")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont('Arial', 10))
        self.status_label.setStyleSheet("color: #999999; margin-top: 10px;")
        main_layout.addWidget(self.status_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Thêm shortcuts
        QShortcut(QKeySequence("Ctrl+R"), self, self.start_recording)
        QShortcut(QKeySequence("Ctrl+S"), self, self.stop_recording)
        QShortcut(QKeySequence("Ctrl+V"), self, self.paste_text)

    def start_recording(self):
        try:
            if not self.state_store.get_state('is_recording'):
                self.state_store.set_state('is_recording', True)
                self.docs_controller.start_voice_typing()
                self.recording_seconds = 0
                self.recording_timer.start(1000)
                self.status_label.setText("Đang ghi âm: 00:00")
                QMessageBox.information(self, "Thông báo", "Bắt đầu ghi âm")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể bắt đầu ghi âm: {str(e)}")

    def stop_recording(self):
        try:
            if self.state_store.get_state('is_recording'):
                self.state_store.set_state('is_recording', False)
                self.docs_controller.stop_voice_typing()
                self.recording_timer.stop()
                self.status_label.setText("Trạng thái: Sẵn sàng")
                QMessageBox.information(self, "Thông báo", "Dừng ghi âm")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể dừng ghi âm: {str(e)}")

    def paste_text(self):
        try:
            self.status_label.setText("Đang xử lý...")
            self.progress_bar.show()
            self.progress_bar.setValue(50)
            
            text = self.docs_controller.get_text()
            self.system_interaction.paste_text(text)
            
            self.progress_bar.setValue(100)
            self.status_label.setText("Trạng thái: Sẵn sàng")
            QMessageBox.information(self, "Thông báo", "Đã dán văn bản")
            
            # Ẩn thanh tiến trình sau 1 giây
            QTimer.singleShot(1000, self.progress_bar.hide)
        except Exception as e:
            self.status_label.setText("Trạng thái: Lỗi")
            self.progress_bar.hide()
            QMessageBox.critical(self, "Lỗi", f"Không thể dán văn bản: {str(e)}")

    def preview_text(self):
        try:
            text = self.docs_controller.get_text()
            if text:
                QMessageBox.information(self, "Xem trước văn bản", text)
            else:
                QMessageBox.information(self, "Thông báo", "Chưa có văn bản nào được ghi")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể xem trước văn bản: {str(e)}")

    def update_timer(self):
        self.recording_seconds += 1
        minutes = self.recording_seconds // 60
        seconds = self.recording_seconds % 60
        self.status_label.setText(f"Đang ghi âm: {minutes:02d}:{seconds:02d}")