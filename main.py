"""
VoiceTyping - Ứng dụng nhập văn bản bằng giọng nói
Entry point của ứng dụng với các cấu hình khởi tạo cần thiết
"""

import sys
import os

# High DPI support cho màn hình độ phân giải cao
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFont

# Enable High DPI trước khi tạo QApplication
QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

from frontend.main_window import MainWindow


def main():
    """Khởi chạy ứng dụng"""
    app = QApplication(sys.argv)
    
    # Thiết lập thông tin ứng dụng
    app.setApplicationName("VoiceTyping")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("VoiceTyping")
    
    # Thiết lập font mặc định
    font = QFont("Segoe UI", 10)
    font.setStyleHint(QFont.SansSerif)
    app.setFont(font)
    
    # Tạo và hiển thị cửa sổ chính
    window = MainWindow()
    window.show()
    
    # Chạy event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
