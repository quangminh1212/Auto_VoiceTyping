"""
VoiceTyping - Giao diện người dùng theo phong cách Google Sound Bars
Frameless window, custom title bar, dual theme (light/dark), animated sound bars
"""

import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, 
                             QProgressBar, QComboBox, QSystemTrayIcon, QMenu, QAction,
                             QGraphicsDropShadowEffect, QSizePolicy)
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty, QPoint
from PyQt5.QtGui import (QIcon, QPalette, QColor, QFont, QPainter, QPixmap,
                          QLinearGradient, QBrush, QPainterPath, QFontDatabase, QRegion)
from backend.controller import InputController
from backend.recognizer import SpeechRecognizer, RecognitionEngine


# ============================================================
# Theme System - Dual theme với palette 4 màu Google
# ============================================================

class ThemeColors:
    """Bảng màu theo phong cách Google Sound Bars, hỗ trợ light/dark"""
    
    # Google Accent Colors (cố định cả 2 theme, lấy từ logo)
    BLUE = "#4285F4"
    BLUE_HOVER = "#5A95F5"
    BLUE_LIGHT = "#D2E3FC"
    BLUE_DARK_BG = "#394457"
    GREEN = "#34A853"
    GREEN_HOVER = "#46B864"
    GREEN_LIGHT = "#CEEAD6"
    GREEN_DARK_BG = "#2D4A37"
    RED = "#EA4335"
    RED_HOVER = "#EC5B4E"
    RED_LIGHT = "#FAD2CF"
    RED_DARK_BG = "#4A2D2A"
    YELLOW = "#FBBC04"
    YELLOW_HOVER = "#FCC934"

    # Theme-specific colors
    THEMES = {
        "light": {
            "BG_MAIN":       "#FFFFFF",
            "BG_SURFACE":    "#F8F9FA",
            "BG_ELEVATED":   "#F1F3F4",
            "BG_HOVER":      "#E8EAED",
            "BG_ACTIVE":     "#DADCE0",
            "BORDER":        "#DADCE0",
            "DIVIDER":       "#E8EAED",
            "TEXT_PRIMARY":  "#202124",
            "TEXT_SECONDARY":"#5F6368",
            "TEXT_DISABLED": "#9AA0A6",
            "SELECTED":     "#D2E3FC",
            "SELECTED_HOVER":"#AECBFA",
            "SHADOW_ALPHA":  30,
            "TITLE_BAR":     "#F8F9FA",
        },
        "dark": {
            "BG_MAIN":       "#1E1E1E",
            "BG_SURFACE":    "#2A2A2A",
            "BG_ELEVATED":   "#333333",
            "BG_HOVER":      "#3C3C3C",
            "BG_ACTIVE":     "#484848",
            "BORDER":        "#444444",
            "DIVIDER":       "#3C3C3C",
            "TEXT_PRIMARY":  "#E8EAED",
            "TEXT_SECONDARY":"#9AA0A6",
            "TEXT_DISABLED": "#5F6368",
            "SELECTED":     "#394457",
            "SELECTED_HOVER":"#44526A",
            "SHADOW_ALPHA":  60,
            "TITLE_BAR":     "#2A2A2A",
        },
    }


class Theme:
    """Singleton quản lý theme hiện tại"""
    _current = "light"
    
    @classmethod
    def current(cls):
        return cls._current
    
    @classmethod
    def toggle(cls):
        cls._current = "dark" if cls._current == "light" else "light"
        return cls._current
    
    @classmethod
    def get(cls, key):
        return ThemeColors.THEMES[cls._current][key]
    
    @classmethod
    def is_dark(cls):
        return cls._current == "dark"


# ============================================================
# Custom Widgets
# ============================================================

class SoundBarsWidget(QWidget):
    """Widget vẽ các thanh sóng âm thanh giống logo, animated khi active"""
    
    BAR_COLORS = [ThemeColors.BLUE, ThemeColors.GREEN, ThemeColors.YELLOW, ThemeColors.RED, ThemeColors.BLUE]
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
        self.apply_theme()
    
    def apply_theme(self):
        self.setStyleSheet(f"""
            QProgressBar {{
                background-color: {Theme.get('BG_ELEVATED')};
                border: none;
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ThemeColors.BLUE},
                    stop:0.33 {ThemeColors.GREEN},
                    stop:0.66 {ThemeColors.YELLOW},
                    stop:1 {ThemeColors.RED});
                border-radius: 3px;
            }}
        """)


class StatusIndicator(QWidget):
    """Indicator trạng thái với animation pulse"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(14, 14)
        self._color = Theme.get('TEXT_DISABLED')
        self._is_active = False
        
        self._opacity = 1.0
        self._animation = QTimer()
        self._animation.timeout.connect(self._pulse)
        self._pulse_direction = -1
    
    def set_active(self, active: bool):
        self._is_active = active
        if active:
            self._color = ThemeColors.GREEN
            self._animation.start(50)
        else:
            self._color = Theme.get('TEXT_DISABLED')
            self._animation.stop()
            self._opacity = 1.0
        self.update()
    
    def set_recording(self, recording: bool):
        if recording:
            self._color = ThemeColors.RED
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
    
    def apply_theme(self):
        if not self._is_active:
            self._color = Theme.get('TEXT_DISABLED')
            self.update()


class ModernButton(QPushButton):
    """Button với phong cách Google Material, hỗ trợ theme"""
    
    def __init__(self, text, parent=None, primary=False, danger=False):
        super().__init__(text, parent)
        self.primary = primary
        self.danger = danger
        self.setFixedHeight(42)
        self.setCursor(Qt.PointingHandCursor)
        self._update_style()
        
    def _update_style(self):
        if self.danger:
            bg = ThemeColors.RED
            bg_hover = ThemeColors.RED_HOVER
            text_color = "#FFFFFF"
        elif self.primary:
            bg = ThemeColors.BLUE
            bg_hover = ThemeColors.BLUE_HOVER
            text_color = "#FFFFFF"
        else:
            bg = Theme.get('BG_ELEVATED')
            bg_hover = Theme.get('BG_HOVER')
            text_color = Theme.get('TEXT_PRIMARY')
        
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
                background-color: {Theme.get('BG_ACTIVE') if not self.primary and not self.danger else bg};
            }}
            QPushButton:disabled {{
                background-color: {Theme.get('BG_ELEVATED')};
                color: {Theme.get('TEXT_DISABLED')};
            }}
        """)


class ModernComboBox(QComboBox):
    """ComboBox với phong cách Google Material, hỗ trợ theme"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)
        self.setCursor(Qt.PointingHandCursor)
        self.apply_theme()
    
    def apply_theme(self):
        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {Theme.get('BG_SURFACE')};
                color: {Theme.get('TEXT_PRIMARY')};
                border: 1px solid {Theme.get('BORDER')};
                border-radius: 18px;
                padding: 6px 14px;
                font-size: 13px;
            }}
            QComboBox:hover {{
                background-color: {Theme.get('BG_ELEVATED')};
                border-color: {ThemeColors.BLUE};
            }}
            QComboBox:focus {{
                border-color: {ThemeColors.BLUE};
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
                border-top: 6px solid {Theme.get('TEXT_SECONDARY')};
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Theme.get('BG_MAIN')};
                color: {Theme.get('TEXT_PRIMARY')};
                border: 1px solid {Theme.get('BORDER')};
                border-radius: 12px;
                padding: 4px;
                selection-background-color: {Theme.get('SELECTED')};
                selection-color: {ThemeColors.BLUE};
            }}
            QComboBox QAbstractItemView::item {{
                padding: 8px 14px;
                border-radius: 8px;
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: {Theme.get('BG_HOVER')};
            }}
        """)


# ============================================================
# Main Window - Frameless, Custom Title Bar, Dual Theme
# ============================================================

class MainWindow(QMainWindow):
    """Giao diện chính - Frameless, Custom Title Bar, Google Sound Bars Theme"""
    
    TITLE_BAR_HEIGHT = 40
    BORDER_RADIUS = 16
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoiceTyping")
        self.setMinimumSize(440, 400)
        self.setMaximumSize(600, 540)
        
        # Frameless window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Tìm logo file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._logo_path = os.path.join(base_dir, "logo.png")
        ico_path = os.path.join(base_dir, "logo.ico")
        
        if os.path.exists(ico_path):
            self.setWindowIcon(QIcon(ico_path))
        elif os.path.exists(self._logo_path):
            self.setWindowIcon(QIcon(self._logo_path))
        
        # Thu thập tất cả widget cần apply theme
        self._themed_widgets = []
        
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
        
        # Resize support
        self._resize_edge = None
        self._resize_margin = 6
    
    # ===== Tray =====
    
    def setup_tray(self):
        """Thiết lập System Tray Icon"""
        self.tray_icon = QSystemTrayIcon(self)
        
        ico_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logo.ico")
        if os.path.exists(ico_path):
            self.tray_icon.setIcon(QIcon(ico_path))
        elif os.path.exists(self._logo_path):
            self.tray_icon.setIcon(QIcon(self._logo_path))
        
        self.tray_icon.setToolTip("VoiceTyping - Nhập văn bản bằng giọng nói")
        
        tray_menu = QMenu()
        self._tray_menu = tray_menu
        self._apply_tray_theme()
        
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
    
    def _apply_tray_theme(self):
        self._tray_menu.setStyleSheet(f"""
            QMenu {{
                background-color: {Theme.get('BG_MAIN')};
                color: {Theme.get('TEXT_PRIMARY')};
                border: 1px solid {Theme.get('BORDER')};
                border-radius: 12px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 8px 20px;
                border-radius: 6px;
            }}
            QMenu::item:selected {{
                background-color: {ThemeColors.BLUE_LIGHT if not Theme.is_dark() else ThemeColors.BLUE_DARK_BG};
                color: {ThemeColors.BLUE};
            }}
        """)
    
    def show_window(self):
        self.show()
        self.activateWindow()
        self.raise_()
    
    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()
        elif reason == QSystemTrayIcon.Trigger:
            if self.toggle_btn.text().startswith("🎤"):
                self.start_recognition()
            else:
                self.stop_recognition()
    
    def quit_app(self):
        self.recognizer.cleanup()
        self.tray_icon.hide()
        QApplication.quit()
    
    def changeEvent(self, event):
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
    
    # ===== UI Setup =====
    
    def setup_ui(self):
        """Thiết lập giao diện - Frameless + Custom Title Bar"""
        # Outer wrapper (transparent background for rounded corners)
        outer = QWidget()
        outer.setObjectName("outerWrapper")
        self.setCentralWidget(outer)
        
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        
        # Main container với bo tròn
        self._container = QWidget()
        self._container.setObjectName("mainContainer")
        outer_layout.addWidget(self._container)
        
        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, Theme.get('SHADOW_ALPHA')))
        shadow.setOffset(0, 4)
        self._container.setGraphicsEffect(shadow)
        
        container_layout = QVBoxLayout(self._container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # ===== Custom Title Bar =====
        self._title_bar = self._create_title_bar()
        container_layout.addWidget(self._title_bar)
        
        # ===== Content Area =====
        content = QWidget()
        content.setObjectName("contentArea")
        container_layout.addWidget(content)
        
        self._content_widget = content
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 12, 24, 20)
        content_layout.setSpacing(14)
        
        # Center: Sound Bars + Status
        center_layout = self._create_center_section()
        content_layout.addLayout(center_layout)
        
        # Audio Level
        self.audio_level_bar = AudioLevelBar()
        self._themed_widgets.append(self.audio_level_bar)
        content_layout.addWidget(self.audio_level_bar)
        
        # Controls
        controls = self._create_controls()
        content_layout.addLayout(controls)
        
        # Settings
        settings = self._create_settings()
        content_layout.addLayout(settings)
        
        content_layout.addStretch()
        
        # Footer
        footer = self._create_footer()
        content_layout.addLayout(footer)
        
        # Apply theme lần đầu
        self._apply_container_theme()
    
    def _create_title_bar(self) -> QWidget:
        """Custom title bar thay thế title bar mặc định"""
        bar = QWidget()
        bar.setObjectName("titleBar")
        bar.setFixedHeight(self.TITLE_BAR_HEIGHT)
        
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 8, 0)
        layout.setSpacing(8)
        
        # Logo image
        self._logo_label = QLabel()
        if os.path.exists(self._logo_path):
            pixmap = QPixmap(self._logo_path)
            self._logo_label.setPixmap(pixmap.scaled(22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self._logo_label.setFixedSize(24, 24)
        layout.addWidget(self._logo_label)
        
        # Status indicator
        self.status_indicator = StatusIndicator()
        self._themed_widgets.append(self.status_indicator)
        layout.addWidget(self.status_indicator)
        
        # Title text
        self._title_label = QLabel("VoiceTyping")
        self._title_label.setObjectName("titleLabel")
        layout.addWidget(self._title_label)
        
        layout.addStretch()
        
        # Theme toggle button (sun/moon)
        self._theme_btn = QPushButton("🌙")
        self._theme_btn.setObjectName("titleBtn")
        self._theme_btn.setFixedSize(30, 30)
        self._theme_btn.setCursor(Qt.PointingHandCursor)
        self._theme_btn.setToolTip("Chuyển chế độ sáng/tối")
        self._theme_btn.clicked.connect(self._toggle_theme)
        layout.addWidget(self._theme_btn)
        
        # Minimize button
        self._min_btn = QPushButton("─")
        self._min_btn.setObjectName("titleBtn")
        self._min_btn.setFixedSize(30, 30)
        self._min_btn.setCursor(Qt.PointingHandCursor)
        self._min_btn.setToolTip("Thu nhỏ")
        self._min_btn.clicked.connect(self.showMinimized)
        layout.addWidget(self._min_btn)
        
        # Close button
        self._close_btn = QPushButton("✕")
        self._close_btn.setObjectName("closeBtn")
        self._close_btn.setFixedSize(30, 30)
        self._close_btn.setCursor(Qt.PointingHandCursor)
        self._close_btn.setToolTip("Đóng")
        self._close_btn.clicked.connect(self.close)
        layout.addWidget(self._close_btn)
        
        return bar
    
    def _create_center_section(self) -> QVBoxLayout:
        """Phần trung tâm: Sound Bars + Status"""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)
        
        # Sound Bars widget
        bars_container = QHBoxLayout()
        bars_container.setAlignment(Qt.AlignCenter)
        self.sound_bars = SoundBarsWidget(size=56)
        bars_container.addWidget(self.sound_bars)
        layout.addLayout(bars_container)
        
        # Status label
        self.status_label = QLabel("Sẵn sàng")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Last recognized text
        self.last_text_label = QLabel("")
        self.last_text_label.setObjectName("lastTextLabel")
        self.last_text_label.setWordWrap(True)
        self.last_text_label.setAlignment(Qt.AlignCenter)
        self.last_text_label.setMinimumHeight(50)
        self.last_text_label.setMaximumHeight(120)
        self.last_text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.last_text_label.hide()
        layout.addWidget(self.last_text_label)
        
        return layout
    
    def _create_controls(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignCenter)
        
        self.toggle_btn = ModernButton("🎤 Bắt đầu", primary=True)
        self.toggle_btn.setMinimumWidth(180)
        self.toggle_btn.clicked.connect(self.toggle_recognition)
        self._themed_widgets.append(self.toggle_btn)
        layout.addWidget(self.toggle_btn)
        
        return layout
    
    def _create_settings(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(12)
        
        self._lang_label = QLabel("Ngôn ngữ:")
        self._lang_label.setObjectName("settingsLabel")
        layout.addWidget(self._lang_label)
        
        self.lang_combo = ModernComboBox()
        self.lang_combo.addItems(["Tiếng Việt", "English"])
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        self._themed_widgets.append(self.lang_combo)
        layout.addWidget(self.lang_combo)
        
        layout.addStretch()
        
        self._engine_label = QLabel("Engine:")
        self._engine_label.setObjectName("settingsLabel")
        layout.addWidget(self._engine_label)
        
        self.engine_combo = ModernComboBox()
        self.engine_combo.addItems(["Google", "Whisper", "Faster-Whisper"])
        self.engine_combo.currentIndexChanged.connect(self.on_engine_changed)
        self._themed_widgets.append(self.engine_combo)
        layout.addWidget(self.engine_combo)
        
        return layout
    
    def _create_footer(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        
        self._hint_label = QLabel("💡 Giữ phím Alt để nói")
        self._hint_label.setObjectName("footerLabel")
        layout.addWidget(self._hint_label)
        
        layout.addStretch()
        
        self._version_label = QLabel("v1.0.0")
        self._version_label.setObjectName("footerLabel")
        layout.addWidget(self._version_label)
        
        return layout
    
    def setup_connections(self):
        pass
    
    # ===== Theme Management =====
    
    def _toggle_theme(self):
        """Chuyển đổi giữa light và dark theme"""
        Theme.toggle()
        self._theme_btn.setText("☀️" if Theme.is_dark() else "🌙")
        self._apply_all_theme()
    
    def _apply_all_theme(self):
        """Áp dụng theme cho toàn bộ giao diện"""
        self._apply_container_theme()
        self._apply_tray_theme()
        
        # Apply cho các widget có method apply_theme
        for w in self._themed_widgets:
            if hasattr(w, 'apply_theme'):
                w.apply_theme()
            elif isinstance(w, ModernButton):
                w._update_style()
    
    def _apply_container_theme(self):
        """Áp dụng style cho container chính và tất cả label"""
        r = self.BORDER_RADIUS
        
        self._container.setStyleSheet(f"""
            #mainContainer {{
                background-color: {Theme.get('BG_MAIN')};
                border-radius: {r}px;
                border: 1px solid {Theme.get('BORDER')};
            }}
            #titleBar {{
                background-color: {Theme.get('TITLE_BAR')};
                border-top-left-radius: {r}px;
                border-top-right-radius: {r}px;
                border-bottom: 1px solid {Theme.get('DIVIDER')};
            }}
            #titleLabel {{
                color: {Theme.get('TEXT_PRIMARY')};
                font-size: 14px;
                font-weight: 700;
                background: transparent;
            }}
            #titleBtn {{
                background-color: transparent;
                color: {Theme.get('TEXT_SECONDARY')};
                border: none;
                border-radius: 15px;
                font-size: 13px;
            }}
            #titleBtn:hover {{
                background-color: {Theme.get('BG_HOVER')};
            }}
            #closeBtn {{
                background-color: transparent;
                color: {Theme.get('TEXT_SECONDARY')};
                border: none;
                border-radius: 15px;
                font-size: 13px;
            }}
            #closeBtn:hover {{
                background-color: {ThemeColors.RED_LIGHT if not Theme.is_dark() else ThemeColors.RED_DARK_BG};
                color: {ThemeColors.RED};
            }}
            #contentArea {{
                background-color: {Theme.get('BG_MAIN')};
                border-bottom-left-radius: {r}px;
                border-bottom-right-radius: {r}px;
            }}
            #statusLabel {{
                color: {Theme.get('TEXT_SECONDARY')};
                font-size: 14px;
                font-weight: 500;
                background: transparent;
            }}
            #lastTextLabel {{
                color: {Theme.get('TEXT_PRIMARY')};
                font-size: 13px;
                background-color: {Theme.get('BG_SURFACE')};
                padding: 12px 16px;
                border-radius: 12px;
                border: 1px solid {Theme.get('DIVIDER')};
            }}
            #settingsLabel {{
                color: {Theme.get('TEXT_SECONDARY')};
                font-size: 13px;
                background: transparent;
            }}
            #footerLabel {{
                color: {Theme.get('TEXT_DISABLED')};
                font-size: 11px;
                background: transparent;
            }}
        """)
    
    # ===== Event Handlers =====
    
    def toggle_recognition(self):
        if self.toggle_btn.text().startswith("🎤"):
            self.start_recognition()
        else:
            self.stop_recognition()
    
    def on_alt_pressed(self, pressed: bool):
        if pressed:
            self.start_recognition()
        else:
            self.stop_recognition()
    
    def start_recognition(self):
        self.toggle_btn.setText("⏹ Dừng")
        self.toggle_btn.primary = False
        self.toggle_btn.danger = True
        self.toggle_btn._update_style()
        self.status_indicator.set_recording(True)
        self.sound_bars.set_recording(True)
        self.recognizer.start_listening()
    
    def stop_recognition(self):
        self.toggle_btn.setText("🎤 Bắt đầu")
        self.toggle_btn.primary = True
        self.toggle_btn.danger = False
        self.toggle_btn._update_style()
        self.status_indicator.set_active(False)
        self.sound_bars.set_active(False)
        self.recognizer.stop_listening()
        self.audio_level_bar.setValue(0)
    
    def on_listening_started(self):
        self.status_indicator.set_recording(True)
        self.sound_bars.set_recording(True)
    
    def on_listening_stopped(self):
        self.status_indicator.set_active(False)
        self.sound_bars.set_active(False)
    
    def on_status_changed(self, status: str):
        self.status_label.setText(status)
    
    def on_error(self, error: str):
        self.status_label.setText(f"❌ {error}")
        self.status_label.setStyleSheet(f"color: {ThemeColors.RED}; font-size: 14px; font-weight: 500; background: transparent;")
        QTimer.singleShot(3000, lambda: self.status_label.setStyleSheet(
            f"color: {Theme.get('TEXT_SECONDARY')}; font-size: 14px; font-weight: 500; background: transparent;"
        ))
    
    def on_audio_level(self, level: float):
        self.audio_level_bar.setValue(int(level * 100))
    
    def on_text_recognized(self, text: str):
        self.last_text_label.setText(f'"{text}"')
        self.last_text_label.show()
        QTimer.singleShot(5000, self.last_text_label.hide)
    
    def on_language_changed(self, index: int):
        languages = ["vi-VN", "en-US"]
        self.recognizer.set_language(languages[index])
    
    def on_engine_changed(self, index: int):
        engines = [RecognitionEngine.GOOGLE, RecognitionEngine.WHISPER, RecognitionEngine.FASTER_WHISPER]
        self.recognizer.set_engine(engines[index])
    
    # ===== Window Drag (trên title bar) =====
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Chỉ cho kéo trên vùng title bar
            if event.pos().y() <= self.TITLE_BAR_HEIGHT:
                self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        self._drag_pos = None
    
    def closeEvent(self, event):
        self.recognizer.cleanup()
        event.accept()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())