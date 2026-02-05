"""
VoiceTyping - Giao diện người dùng theo phong cách Google Drive
UI hiện đại với dark theme, animations và hiệu ứng chuyên nghiệp
"""

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, 
                             QProgressBar, QComboBox, QSystemTrayIcon, QMenu, QAction,
                             QGraphicsDropShadowEffect, QSizePolicy)
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import (QIcon, QPalette, QColor, QFont, QPainter, 
                          QLinearGradient, QBrush, QPainterPath, QFontDatabase)
from backend.controller import InputController
from backend.recognizer import SpeechRecognizer, RecognitionEngine


# Google Drive Dark Theme Colors
class Colors:
    """Bảng màu theo phong cách Google Drive Dark Mode"""
    # Backgrounds
    BG_MAIN = "#1f1f1f"
    BG_SURFACE = "#2d2d2d"
    BG_ELEVATED = "#353535"
    BG_HOVER = "#3c4043"
    BG_ACTIVE = "#4a4e51"
    
    # Borders
    BORDER = "#5f6368"
    DIVIDER = "#3c4043"
    
    # Text
    TEXT_PRIMARY = "#e8eaed"
    TEXT_SECONDARY = "#bdc1c6"
    TEXT_DISABLED = "#5f6368"
    
    # Accent Colors
    BLUE = "#8ab4f8"
    BLUE_HOVER = "#aecbfa"
    GREEN = "#81c995"
    GREEN_HOVER = "#a8dab5"
    RED = "#f28b82"
    RED_HOVER = "#f6aca8"
    YELLOW = "#fdd663"
    
    # Selection
    SELECTED = "#394457"
    SELECTED_HOVER = "#44526a"


class AudioLevelBar(QProgressBar):
    """Thanh hiển thị mức âm thanh với animation"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        self.setTextVisible(False)
        self.setFixedHeight(6)
        
        self.setStyleSheet(f"""
            QProgressBar {{
                background-color: {Colors.BG_SURFACE};
                border: none;
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {Colors.BLUE},
                    stop:0.5 {Colors.GREEN},
                    stop:1 {Colors.YELLOW});
                border-radius: 3px;
            }}
        """)


class StatusIndicator(QWidget):
    """Indicator trạng thái với animation pulse"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(12, 12)
        self._color = Colors.TEXT_DISABLED
        self._is_active = False
        
        # Animation cho pulse effect
        self._opacity = 1.0
        self._animation = QTimer()
        self._animation.timeout.connect(self._pulse)
        self._pulse_direction = -1
    
    def set_active(self, active: bool):
        self._is_active = active
        if active:
            self._color = Colors.GREEN
            self._animation.start(50)
        else:
            self._color = Colors.TEXT_DISABLED
            self._animation.stop()
            self._opacity = 1.0
        self.update()
    
    def set_recording(self, recording: bool):
        if recording:
            self._color = Colors.RED
            self._animation.start(50)
        else:
            self.set_active(False)
    
    def _pulse(self):
        self._opacity += 0.05 * self._pulse_direction
        if self._opacity <= 0.4:
            self._pulse_direction = 1
        elif self._opacity >= 1.0:
            self._pulse_direction = -1
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Vẽ vòng tròn với opacity
        painter.setOpacity(self._opacity)
        painter.setBrush(QColor(self._color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(2, 2, 8, 8)
        
        # Vẽ glow effect nếu đang active
        if self._is_active:
            painter.setOpacity(self._opacity * 0.3)
            painter.drawEllipse(0, 0, 12, 12)


class ModernButton(QPushButton):
    """Button với phong cách Google Drive"""
    
    def __init__(self, text, parent=None, primary=False, danger=False):
        super().__init__(text, parent)
        self.primary = primary
        self.danger = danger
        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        self._update_style()
        
    def _update_style(self):
        if self.danger:
            bg = Colors.RED
            bg_hover = Colors.RED_HOVER
        elif self.primary:
            bg = Colors.BLUE
            bg_hover = Colors.BLUE_HOVER
        else:
            bg = Colors.BG_ELEVATED
            bg_hover = Colors.BG_HOVER
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {Colors.TEXT_PRIMARY if not self.primary and not self.danger else Colors.BG_MAIN};
                border: none;
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {bg_hover};
            }}
            QPushButton:pressed {{
                background-color: {Colors.BG_ACTIVE if not self.primary else bg};
            }}
            QPushButton:disabled {{
                background-color: {Colors.BG_SURFACE};
                color: {Colors.TEXT_DISABLED};
            }}
        """)


class ModernComboBox(QComboBox):
    """ComboBox với phong cách Google Drive"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)
        self.setCursor(Qt.PointingHandCursor)
        
        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_ELEVATED};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 13px;
            }}
            QComboBox:hover {{
                background-color: {Colors.BG_HOVER};
                border-color: {Colors.BLUE};
            }}
            QComboBox:focus {{
                border-color: {Colors.BLUE};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid {Colors.TEXT_SECONDARY};
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Colors.BG_SURFACE};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 8px;
                padding: 4px;
                selection-background-color: {Colors.SELECTED};
            }}
            QComboBox QAbstractItemView::item {{
                padding: 8px 12px;
                border-radius: 4px;
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: {Colors.BG_HOVER};
            }}
        """)


class MainWindow(QMainWindow):
    """Giao diện chính với phong cách Google Drive"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoiceTyping")
        self.setMinimumSize(380, 280)
        self.setMaximumSize(500, 400)
        self.setWindowIcon(QIcon("logo.ico"))
        
        # Flags - Giữ cửa sổ luôn trên cùng
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        self.setup_ui()
        self.setup_tray()
        self.setup_connections()
        
        # Controllers
        self.input_controller = InputController()
        self.recognizer = SpeechRecognizer()
        
        # Kết nối signals
        self.input_controller.alt_pressed.connect(self.on_alt_pressed)
        self.recognizer.text_recognized.connect(self.input_controller.type_text)
        self.recognizer.text_recognized.connect(self.on_text_recognized)
        self.recognizer.status_changed.connect(self.on_status_changed)
        self.recognizer.error_occurred.connect(self.on_error)
        self.recognizer.audio_level.connect(self.on_audio_level)
        self.recognizer.listening_started.connect(self.on_listening_started)
        self.recognizer.listening_stopped.connect(self.on_listening_stopped)
        
        # Drag support
        self._drag_pos = None
    
    def setup_tray(self):
        """Thiết lập System Tray Icon"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("logo.ico"))
        self.tray_icon.setToolTip("VoiceTyping - Nhập văn bản bằng giọng nói")
        
        # Tạo menu cho tray
        tray_menu = QMenu()
        tray_menu.setStyleSheet(f"""
            QMenu {{
                background-color: {Colors.BG_SURFACE};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 8px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 8px 20px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {Colors.BG_HOVER};
            }}
        """)
        
        # Actions
        show_action = tray_menu.addAction("🖥️ Hiển thị")
        show_action.triggered.connect(self.show_window)
        
        start_action = tray_menu.addAction("🎤 Bắt đầu nghe")
        start_action.triggered.connect(self.start_recognition)
        
        stop_action = tray_menu.addAction("⏹ Dừng nghe")
        stop_action.triggered.connect(self.stop_recognition)
        
        tray_menu.addSeparator()
        
        quit_action = tray_menu.addAction("❌ Thoát")
        quit_action.triggered.connect(self.quit_app)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()
    
    def show_window(self):
        """Hiển thị cửa sổ từ tray"""
        self.show()
        self.activateWindow()
        self.raise_()
    
    def on_tray_activated(self, reason):
        """Xử lý khi click vào tray icon"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()
        elif reason == QSystemTrayIcon.Trigger:
            # Single click - toggle listening
            if self.toggle_btn.text().startswith("🎤"):
                self.start_recognition()
            else:
                self.stop_recognition()
    
    def quit_app(self):
        """Thoát ứng dụng hoàn toàn"""
        self.recognizer.cleanup()
        self.tray_icon.hide()
        QApplication.quit()
    
    def changeEvent(self, event):
        """Minimize vào tray thay vì taskbar"""
        if event.type() == event.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                self.hide()
                self.tray_icon.showMessage(
                    "VoiceTyping",
                    "Ứng dụng đang chạy ở khay hệ thống.\nNhấn đúp để mở lại hoặc click để bật/tắt micro.",
                    QSystemTrayIcon.Information,
                    2000
                )
        super().changeEvent(event)
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Main container với rounded corners và shadow
        container = QWidget()
        container.setObjectName("mainContainer")
        container.setStyleSheet(f"""
            #mainContainer {{
                background-color: {Colors.BG_MAIN};
                border-radius: 16px;
                border: 1px solid {Colors.DIVIDER};
            }}
        """)
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        container.setGraphicsEffect(shadow)
        
        self.setCentralWidget(container)
        
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)
        
        # ===== Header =====
        header = self._create_header()
        main_layout.addLayout(header)
        
        # ===== Divider =====
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background-color: {Colors.DIVIDER};")
        main_layout.addWidget(divider)
        
        # ===== Status Section =====
        status_section = self._create_status_section()
        main_layout.addLayout(status_section)
        
        # ===== Audio Level =====
        self.audio_level_bar = AudioLevelBar()
        main_layout.addWidget(self.audio_level_bar)
        
        # ===== Controls =====
        controls = self._create_controls()
        main_layout.addLayout(controls)
        
        # ===== Settings =====
        settings = self._create_settings()
        main_layout.addLayout(settings)
        
        main_layout.addStretch()
        
        # ===== Footer =====
        footer = self._create_footer()
        main_layout.addLayout(footer)
    
    def _create_header(self) -> QHBoxLayout:
        """Tạo header với title và nút đóng"""
        layout = QHBoxLayout()
        
        # Logo và Title
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        
        # Status indicator
        self.status_indicator = StatusIndicator()
        title_layout.addWidget(self.status_indicator)
        
        # Title
        title = QLabel("VoiceTyping")
        title.setStyleSheet(f"""
            color: {Colors.TEXT_PRIMARY};
            font-size: 18px;
            font-weight: 600;
        """)
        title_layout.addWidget(title)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Minimize button
        min_btn = QPushButton("─")
        min_btn.setFixedSize(32, 32)
        min_btn.setCursor(Qt.PointingHandCursor)
        min_btn.clicked.connect(self.showMinimized)
        min_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Colors.TEXT_SECONDARY};
                border: none;
                border-radius: 6px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {Colors.BG_HOVER};
            }}
        """)
        layout.addWidget(min_btn)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Colors.TEXT_SECONDARY};
                border: none;
                border-radius: 6px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {Colors.RED};
                color: white;
            }}
        """)
        layout.addWidget(close_btn)
        
        return layout
    
    def _create_status_section(self) -> QVBoxLayout:
        """Tạo phần hiển thị trạng thái"""
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Status label
        self.status_label = QLabel("Sẵn sàng")
        self.status_label.setStyleSheet(f"""
            color: {Colors.TEXT_SECONDARY};
            font-size: 14px;
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Last recognized text
        self.last_text_label = QLabel("")
        self.last_text_label.setWordWrap(True)
        self.last_text_label.setStyleSheet(f"""
            color: {Colors.TEXT_PRIMARY};
            font-size: 13px;
            background-color: {Colors.BG_SURFACE};
            padding: 10px 14px;
            border-radius: 8px;
        """)
        self.last_text_label.setAlignment(Qt.AlignCenter)
        self.last_text_label.setMinimumHeight(50)
        self.last_text_label.hide()
        layout.addWidget(self.last_text_label)
        
        return layout
    
    def _create_controls(self) -> QHBoxLayout:
        """Tạo các nút điều khiển"""
        layout = QHBoxLayout()
        layout.setSpacing(12)
        
        # Start/Stop button
        self.toggle_btn = ModernButton("🎤 Bắt đầu", primary=True)
        self.toggle_btn.clicked.connect(self.toggle_recognition)
        layout.addWidget(self.toggle_btn)
        
        return layout
    
    def _create_settings(self) -> QHBoxLayout:
        """Tạo phần cài đặt"""
        layout = QHBoxLayout()
        layout.setSpacing(12)
        
        # Language selector
        lang_label = QLabel("Ngôn ngữ:")
        lang_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(lang_label)
        
        self.lang_combo = ModernComboBox()
        self.lang_combo.addItems(["Tiếng Việt", "English"])
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        layout.addWidget(self.lang_combo)
        
        layout.addStretch()
        
        # Engine selector
        engine_label = QLabel("Engine:")
        engine_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(engine_label)
        
        self.engine_combo = ModernComboBox()
        self.engine_combo.addItems(["Google", "Whisper", "Faster-Whisper"])
        self.engine_combo.currentIndexChanged.connect(self.on_engine_changed)
        layout.addWidget(self.engine_combo)
        
        return layout
    
    def _create_footer(self) -> QHBoxLayout:
        """Tạo footer"""
        layout = QHBoxLayout()
        
        # Shortcut hint
        hint = QLabel("💡 Giữ phím Alt để nói")
        hint.setStyleSheet(f"""
            color: {Colors.TEXT_DISABLED};
            font-size: 12px;
        """)
        layout.addWidget(hint)
        
        layout.addStretch()
        
        # Version
        version = QLabel("v1.0.0")
        version.setStyleSheet(f"""
            color: {Colors.TEXT_DISABLED};
            font-size: 11px;
        """)
        layout.addWidget(version)
        
        return layout
    
    def setup_connections(self):
        """Thiết lập kết nối signals"""
        pass
    
    # ===== Event Handlers =====
    
    def toggle_recognition(self):
        """Bật/tắt nhận dạng giọng nói"""
        if self.toggle_btn.text().startswith("🎤"):
            self.start_recognition()
        else:
            self.stop_recognition()
    
    def on_alt_pressed(self, pressed: bool):
        """Xử lý nhấn phím Alt"""
        if pressed:
            self.start_recognition()
        else:
            self.stop_recognition()
    
    def start_recognition(self):
        """Bắt đầu nhận dạng"""
        self.toggle_btn.setText("⏹ Dừng")
        self.toggle_btn.primary = False
        self.toggle_btn.danger = True
        self.toggle_btn._update_style()
        self.status_indicator.set_recording(True)
        self.recognizer.start_listening()
    
    def stop_recognition(self):
        """Dừng nhận dạng"""
        self.toggle_btn.setText("🎤 Bắt đầu")
        self.toggle_btn.primary = True
        self.toggle_btn.danger = False
        self.toggle_btn._update_style()
        self.status_indicator.set_active(False)
        self.recognizer.stop_listening()
        self.audio_level_bar.setValue(0)
    
    def on_listening_started(self):
        """Xử lý khi bắt đầu lắng nghe"""
        self.status_indicator.set_recording(True)
    
    def on_listening_stopped(self):
        """Xử lý khi dừng lắng nghe"""
        self.status_indicator.set_active(False)
    
    def on_status_changed(self, status: str):
        """Cập nhật trạng thái"""
        self.status_label.setText(status)
    
    def on_error(self, error: str):
        """Hiển thị lỗi"""
        self.status_label.setText(f"❌ {error}")
        self.status_label.setStyleSheet(f"color: {Colors.RED}; font-size: 14px;")
        QTimer.singleShot(3000, lambda: self.status_label.setStyleSheet(
            f"color: {Colors.TEXT_SECONDARY}; font-size: 14px;"
        ))
    
    def on_audio_level(self, level: float):
        """Cập nhật mức âm thanh"""
        self.audio_level_bar.setValue(int(level * 100))
    
    def on_text_recognized(self, text: str):
        """Hiển thị văn bản đã nhận dạng"""
        self.last_text_label.setText(f'"{text}"')
        self.last_text_label.show()
        # Ẩn sau 5 giây
        QTimer.singleShot(5000, self.last_text_label.hide)
    
    def on_language_changed(self, index: int):
        """Đổi ngôn ngữ"""
        languages = ["vi-VN", "en-US"]
        self.recognizer.set_language(languages[index])
    
    def on_engine_changed(self, index: int):
        """Đổi engine nhận dạng"""
        engines = [RecognitionEngine.GOOGLE, RecognitionEngine.WHISPER, RecognitionEngine.FASTER_WHISPER]
        self.recognizer.set_engine(engines[index])
    
    # ===== Window Drag Support =====
    
    def mousePressEvent(self, event):
        """Bắt đầu kéo cửa sổ"""
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Kéo cửa sổ"""
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Kết thúc kéo cửa sổ"""
        self._drag_pos = None
    
    def closeEvent(self, event):
        """Cleanup khi đóng"""
        self.recognizer.cleanup()
        event.accept()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    # Set application font
    app.setFont(QFont("Segoe UI", 10))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())