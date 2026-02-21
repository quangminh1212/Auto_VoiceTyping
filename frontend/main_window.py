"""
VoiceTyping - Giao diện người dùng theo phong cách Google Sound Bars
UI hiện đại với light theme, animations sóng âm thanh và palette 4 màu Google
"""

import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, 
                             QProgressBar, QComboBox, QSystemTrayIcon, QMenu, QAction,
                             QGraphicsDropShadowEffect, QSizePolicy)
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import (QIcon, QPalette, QColor, QFont, QPainter, QPixmap,
                          QLinearGradient, QBrush, QPainterPath, QFontDatabase)
from backend.controller import InputController
from backend.recognizer import SpeechRecognizer, RecognitionEngine


# Google Sound Bars - Light Theme Colors (lấy cảm hứng từ logo)
class Colors:
    """Bảng màu theo phong cách Google Sound Bars trên nền sáng"""
    # Backgrounds - Light
    BG_MAIN = "#FFFFFF"
    BG_SURFACE = "#F8F9FA"
    BG_ELEVATED = "#F1F3F4"
    BG_HOVER = "#E8EAED"
    BG_ACTIVE = "#DADCE0"
    
    # Borders
    BORDER = "#DADCE0"
    DIVIDER = "#E8EAED"
    
    # Text
    TEXT_PRIMARY = "#202124"
    TEXT_SECONDARY = "#5F6368"
    TEXT_DISABLED = "#9AA0A6"
    
    # Google Accent Colors (từ logo)
    BLUE = "#4285F4"
    BLUE_HOVER = "#5A95F5"
    BLUE_LIGHT = "#D2E3FC"
    GREEN = "#34A853"
    GREEN_HOVER = "#46B864"
    GREEN_LIGHT = "#CEEAD6"
    RED = "#EA4335"
    RED_HOVER = "#EC5B4E"
    RED_LIGHT = "#FAD2CF"
    YELLOW = "#FBBC04"
    YELLOW_HOVER = "#FCC934"
    YELLOW_LIGHT = "#FEF7E0"
    
    # Selection
    SELECTED = "#D2E3FC"
    SELECTED_HOVER = "#AECBFA"


class SoundBarsWidget(QWidget):
    """Widget vẽ các thanh sóng âm thanh giống logo, animated khi active"""
    
    # Màu sắc 5 thanh giống logo: xanh dương, xanh lá, vàng, đỏ, xanh dương
    BAR_COLORS = [Colors.BLUE, Colors.GREEN, Colors.YELLOW, Colors.RED, Colors.BLUE]
    # Chiều cao tỉ lệ 5 thanh (tĩnh): ngắn, cao, cao nhất, cao, ngắn
    BASE_HEIGHTS = [0.4, 0.7, 1.0, 0.7, 0.4]
    
    def __init__(self, size=48, parent=None):
        super().__init__(parent)
        self._size = size
        self.setFixedSize(size, size)
        self._is_active = False
        self._is_recording = False
        self._anim_offsets = [0.0] * 5
        self._anim_dirs = [1, -1, 1, -1, 1]
        self._anim_speeds = [0.04, 0.05, 0.03, 0.045, 0.035]
        
        self._timer = QTimer()
        self._timer.timeout.connect(self._animate)
    
    def set_active(self, active: bool):
        self._is_active = active
        if active:
            self._timer.start(40)
        else:
            self._timer.stop()
            self._anim_offsets = [0.0] * 5
        self.update()
    
    def set_recording(self, recording: bool):
        self._is_recording = recording
        if recording:
            self._timer.start(30)
        else:
            self.set_active(False)
    
    def _animate(self):
        for i in range(5):
            self._anim_offsets[i] += self._anim_speeds[i] * self._anim_dirs[i]
            if self._anim_offsets[i] > 0.3:
                self._anim_dirs[i] = -1
            elif self._anim_offsets[i] < -0.3:
                self._anim_dirs[i] = 1
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        s = self._size
        bar_width = s * 0.12
        gap = s * 0.06
        total_w = 5 * bar_width + 4 * gap
        start_x = (s - total_w) / 2
        max_h = s * 0.85
        
        for i in range(5):
            h_ratio = self.BASE_HEIGHTS[i] + self._anim_offsets[i]
            h_ratio = max(0.15, min(1.0, h_ratio))
            h = max_h * h_ratio
            x = start_x + i * (bar_width + gap)
            y = (s - h) / 2
            
            painter.setBrush(QColor(self.BAR_COLORS[i]))
            painter.setPen(Qt.NoPen)
            
            # Vẽ thanh bo tròn giống logo
            radius = bar_width / 2
            path = QPainterPath()
            path.addRoundedRect(x, y, bar_width, h, radius, radius)
            painter.drawPath(path)


class AudioLevelBar(QProgressBar):
    """Thanh hiển thị mức âm thanh với gradient 4 màu Google"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        self.setTextVisible(False)
        self.setFixedHeight(6)
        
        self.setStyleSheet(f"""
            QProgressBar {{
                background-color: {Colors.BG_ELEVATED};
                border: none;
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {Colors.BLUE},
                    stop:0.33 {Colors.GREEN},
                    stop:0.66 {Colors.YELLOW},
                    stop:1 {Colors.RED});
                border-radius: 3px;
            }}
        """)


class StatusIndicator(QWidget):
    """Indicator trạng thái với animation pulse - dùng màu Google"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(14, 14)
        self._color = Colors.TEXT_DISABLED
        self._is_active = False
        
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
        
        painter.setOpacity(self._opacity)
        painter.setBrush(QColor(self._color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(2, 2, 10, 10)
        
        if self._is_active:
            painter.setOpacity(self._opacity * 0.3)
            painter.drawEllipse(0, 0, 14, 14)


class ModernButton(QPushButton):
    """Button với phong cách Google Material trên nền sáng"""
    
    def __init__(self, text, parent=None, primary=False, danger=False):
        super().__init__(text, parent)
        self.primary = primary
        self.danger = danger
        self.setFixedHeight(42)
        self.setCursor(Qt.PointingHandCursor)
        self._update_style()
        
    def _update_style(self):
        if self.danger:
            bg = Colors.RED
            bg_hover = Colors.RED_HOVER
            text_color = "#FFFFFF"
        elif self.primary:
            bg = Colors.BLUE
            bg_hover = Colors.BLUE_HOVER
            text_color = "#FFFFFF"
        else:
            bg = Colors.BG_ELEVATED
            bg_hover = Colors.BG_HOVER
            text_color = Colors.TEXT_PRIMARY
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {text_color};
                border: none;
                border-radius: 21px;
                padding: 8px 28px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {bg_hover};
            }}
            QPushButton:pressed {{
                background-color: {Colors.BG_ACTIVE if not self.primary and not self.danger else bg};
                opacity: 0.9;
            }}
            QPushButton:disabled {{
                background-color: {Colors.BG_ELEVATED};
                color: {Colors.TEXT_DISABLED};
            }}
        """)


class ModernComboBox(QComboBox):
    """ComboBox với phong cách Google Material trên nền sáng"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)
        self.setCursor(Qt.PointingHandCursor)
        
        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_SURFACE};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 18px;
                padding: 6px 14px;
                font-size: 13px;
            }}
            QComboBox:hover {{
                background-color: {Colors.BG_ELEVATED};
                border-color: {Colors.BLUE};
            }}
            QComboBox:focus {{
                border-color: {Colors.BLUE};
                border-width: 2px;
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
                background-color: {Colors.BG_MAIN};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
                padding: 4px;
                selection-background-color: {Colors.SELECTED};
                selection-color: {Colors.BLUE};
            }}
            QComboBox QAbstractItemView::item {{
                padding: 8px 14px;
                border-radius: 8px;
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: {Colors.BG_HOVER};
            }}
        """)


class MainWindow(QMainWindow):
    """Giao diện chính với phong cách Google Sound Bars (Light Theme)"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoiceTyping")
        self.setMinimumSize(440, 380)
        self.setMaximumSize(600, 520)
        
        # Tìm logo file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._logo_path = os.path.join(base_dir, "logo.png")
        ico_path = os.path.join(base_dir, "logo.ico")
        
        if os.path.exists(ico_path):
            self.setWindowIcon(QIcon(ico_path))
        elif os.path.exists(self._logo_path):
            self.setWindowIcon(QIcon(self._logo_path))
        
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
        
        ico_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logo.ico")
        if os.path.exists(ico_path):
            self.tray_icon.setIcon(QIcon(ico_path))
        elif os.path.exists(self._logo_path):
            self.tray_icon.setIcon(QIcon(self._logo_path))
        
        self.tray_icon.setToolTip("VoiceTyping - Nhập văn bản bằng giọng nói")
        
        # Tạo menu cho tray - light theme
        tray_menu = QMenu()
        tray_menu.setStyleSheet(f"""
            QMenu {{
                background-color: {Colors.BG_MAIN};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 8px 20px;
                border-radius: 6px;
            }}
            QMenu::item:selected {{
                background-color: {Colors.BLUE_LIGHT};
                color: {Colors.BLUE};
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
        """Thiết lập giao diện - Google Sound Bars Light Theme"""
        # Main container với nền trắng, bo tròn, shadow
        container = QWidget()
        container.setObjectName("mainContainer")
        container.setStyleSheet(f"""
            #mainContainer {{
                background-color: {Colors.BG_MAIN};
                border-radius: 20px;
                border: 1px solid {Colors.DIVIDER};
            }}
        """)
        
        # Shadow effect - nhẹ nhàng cho light theme
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        container.setGraphicsEffect(shadow)
        
        self.setCentralWidget(container)
        
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)
        
        # ===== Header =====
        header = self._create_header()
        main_layout.addLayout(header)
        
        # ===== Divider =====
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background-color: {Colors.DIVIDER};")
        main_layout.addWidget(divider)
        
        # ===== Center: Sound Bars + Status =====
        center_layout = self._create_center_section()
        main_layout.addLayout(center_layout)
        
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
        """Tạo header với logo PNG, title và nút đóng"""
        layout = QHBoxLayout()
        
        # Logo + Title
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        
        # Logo image từ file
        logo_label = QLabel()
        if os.path.exists(self._logo_path):
            pixmap = QPixmap(self._logo_path)
            logo_label.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setFixedSize(32, 32)
        title_layout.addWidget(logo_label)
        
        # Status indicator (nhỏ, ẩn sau logo)
        self.status_indicator = StatusIndicator()
        title_layout.addWidget(self.status_indicator)
        
        # Title
        title = QLabel("VoiceTyping")
        title.setStyleSheet(f"""
            color: {Colors.TEXT_PRIMARY};
            font-size: 18px;
            font-weight: 700;
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
                border-radius: 16px;
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
                border-radius: 16px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {Colors.RED_LIGHT};
                color: {Colors.RED};
            }}
        """)
        layout.addWidget(close_btn)
        
        return layout
    
    def _create_center_section(self) -> QVBoxLayout:
        """Tạo phần trung tâm với Sound Bars widget và status"""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignCenter)
        
        # Sound Bars widget (animation giống logo)
        bars_container = QHBoxLayout()
        bars_container.setAlignment(Qt.AlignCenter)
        self.sound_bars = SoundBarsWidget(size=56)
        bars_container.addWidget(self.sound_bars)
        layout.addLayout(bars_container)
        
        # Status label
        self.status_label = QLabel("Sẵn sàng")
        self.status_label.setStyleSheet(f"""
            color: {Colors.TEXT_SECONDARY};
            font-size: 14px;
            font-weight: 500;
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
            padding: 12px 16px;
            border-radius: 12px;
            border: 1px solid {Colors.DIVIDER};
        """)
        self.last_text_label.setAlignment(Qt.AlignCenter)
        self.last_text_label.setMinimumHeight(50)
        self.last_text_label.setMaximumHeight(120)
        self.last_text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.last_text_label.hide()
        layout.addWidget(self.last_text_label)
        
        return layout
    
    def _create_controls(self) -> QHBoxLayout:
        """Tạo các nút điều khiển"""
        layout = QHBoxLayout()
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignCenter)
        
        # Start/Stop button - bo tròn pill shape
        self.toggle_btn = ModernButton("🎤 Bắt đầu", primary=True)
        self.toggle_btn.setMinimumWidth(180)
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
        
        # Shortcut hint - dùng tag màu Google
        hint = QLabel("💡 Giữ phím Alt để nói")
        hint.setStyleSheet(f"""
            color: {Colors.TEXT_DISABLED};
            font-size: 12px;
        """)
        layout.addWidget(hint)
        
        layout.addStretch()
        
        # 4 chấm màu Google nhỏ làm trang trí
        dots_label = QLabel("● ● ● ●")
        dots_label.setStyleSheet(f"""
            color: {Colors.TEXT_DISABLED};
            font-size: 6px;
            letter-spacing: 2px;
        """)
        layout.addWidget(dots_label)
        
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
        self.sound_bars.set_recording(True)
        self.recognizer.start_listening()
    
    def stop_recognition(self):
        """Dừng nhận dạng"""
        self.toggle_btn.setText("🎤 Bắt đầu")
        self.toggle_btn.primary = True
        self.toggle_btn.danger = False
        self.toggle_btn._update_style()
        self.status_indicator.set_active(False)
        self.sound_bars.set_active(False)
        self.recognizer.stop_listening()
        self.audio_level_bar.setValue(0)
    
    def on_listening_started(self):
        """Xử lý khi bắt đầu lắng nghe"""
        self.status_indicator.set_recording(True)
        self.sound_bars.set_recording(True)
    
    def on_listening_stopped(self):
        """Xử lý khi dừng lắng nghe"""
        self.status_indicator.set_active(False)
        self.sound_bars.set_active(False)
    
    def on_status_changed(self, status: str):
        """Cập nhật trạng thái"""
        self.status_label.setText(status)
    
    def on_error(self, error: str):
        """Hiển thị lỗi"""
        self.status_label.setText(f"❌ {error}")
        self.status_label.setStyleSheet(f"color: {Colors.RED}; font-size: 14px; font-weight: 500;")
        QTimer.singleShot(3000, lambda: self.status_label.setStyleSheet(
            f"color: {Colors.TEXT_SECONDARY}; font-size: 14px; font-weight: 500;"
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