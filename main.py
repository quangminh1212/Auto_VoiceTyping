"""
VoiceTyping - Ứng dụng nhập văn bản bằng giọng nói
Entry point của ứng dụng với các cấu hình khởi tạo cần thiết
"""

import sys
import os
import tempfile
import atexit

# High DPI support cho màn hình độ phân giải cao
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QCoreApplication, QLockFile
from PyQt5.QtGui import QFont

# Enable High DPI trước khi tạo QApplication
QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class SingleInstance:
    """Đảm bảo chỉ có 1 instance của ứng dụng chạy"""
    
    def __init__(self, app_name="VoiceTyping"):
        self.lock_file_path = os.path.join(tempfile.gettempdir(), f"{app_name}.lock")
        self.lock_file = QLockFile(self.lock_file_path)
        self.is_locked = False
    
    def try_lock(self) -> bool:
        """Thử lock file. Trả về True nếu là instance duy nhất."""
        # Thử lock với timeout 100ms
        self.is_locked = self.lock_file.tryLock(100)
        return self.is_locked
    
    def unlock(self):
        """Giải phóng lock"""
        if self.is_locked:
            self.lock_file.unlock()
            self.is_locked = False
    
    def cleanup(self):
        """Dọn dẹp khi thoát"""
        self.unlock()
        # Xóa file lock nếu tồn tại
        if os.path.exists(self.lock_file_path):
            try:
                os.remove(self.lock_file_path)
            except Exception:
                pass


def main():
    """Khởi chạy ứng dụng"""
    # Tạo QApplication trước để có thể hiển thị dialog
    app = QApplication(sys.argv)
    
    # Kiểm tra single instance
    single_instance = SingleInstance("VoiceTyping")
    
    if not single_instance.try_lock():
        # Đã có instance khác đang chạy
        QMessageBox.warning(
            None,
            "VoiceTyping",
            "Ứng dụng VoiceTyping đã đang chạy!\n\n"
            "Chỉ có thể chạy 1 instance tại một thời điểm.\n"
            "Vui lòng tắt ứng dụng cũ trước khi mở lại.",
            QMessageBox.Ok
        )
        sys.exit(1)
    
    # Đăng ký cleanup khi thoát
    atexit.register(single_instance.cleanup)
    
    # Thiết lập thông tin ứng dụng
    app.setApplicationName("VoiceTyping")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("VoiceTyping")
    
    # Thiết lập font mặc định
    font = QFont("Segoe UI", 10)
    font.setStyleHint(QFont.SansSerif)
    app.setFont(font)
    
    # Import và tạo cửa sổ chính
    from frontend.main_window import MainWindow
    window = MainWindow()
    window.show()
    
    # Chạy event loop
    exit_code = app.exec_()
    
    # Cleanup
    single_instance.cleanup()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
