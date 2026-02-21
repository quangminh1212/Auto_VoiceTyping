"""
VoiceTyping - Ứng dụng nhập văn bản bằng giọng nói
Entry point của ứng dụng với các cấu hình khởi tạo cần thiết
Hot-reload: tự restart khi phát hiện thay đổi file .py
"""

import sys
import os
import tempfile
import atexit
import threading
import time
import glob

# Exit code đặc biệt: signal cho run.bat biết cần hot-reload
EXIT_CODE_RELOAD = 42

# High DPI support cho màn hình độ phân giải cao
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QCoreApplication, QLockFile
from PyQt5.QtGui import QFont

# Enable High DPI trước khi tạo QApplication
QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class FileWatcher(threading.Thread):
    """Theo dõi thay đổi file .py trong dự án, trigger restart khi phát hiện"""
    
    def __init__(self, watch_dir, interval=1.5):
        super().__init__(daemon=True)
        self.watch_dir = watch_dir
        self.interval = interval
        self._stop_event = threading.Event()
        self._snapshots = {}
        self._take_snapshot()
    
    def _get_py_files(self):
        """Lấy danh sách tất cả file .py trong dự án (trừ venv, __pycache__)"""
        py_files = []
        for pattern in ['*.py', 'backend/*.py', 'frontend/*.py']:
            py_files.extend(glob.glob(os.path.join(self.watch_dir, pattern)))
        return py_files
    
    def _take_snapshot(self):
        """Chụp snapshot mtime của tất cả file .py"""
        self._snapshots = {}
        for f in self._get_py_files():
            try:
                self._snapshots[f] = os.stat(f).st_mtime
            except OSError:
                pass
    
    def _check_changes(self):
        """Kiểm tra xem có file nào thay đổi không"""
        for f in self._get_py_files():
            try:
                mtime = os.stat(f).st_mtime
                old_mtime = self._snapshots.get(f)
                if old_mtime is None or mtime != old_mtime:
                    return f
            except OSError:
                continue
        return None
    
    def run(self):
        """Chạy polling loop, khi phát hiện thay đổi → quit app với code 42"""
        # Chờ 3s ban đầu để app khởi tạo xong
        self._stop_event.wait(3)
        
        while not self._stop_event.is_set():
            changed = self._check_changes()
            if changed:
                basename = os.path.basename(changed)
                print(f"\n[HOT-RELOAD] Phát hiện thay đổi: {basename}")
                print("[HOT-RELOAD] Đang khởi động lại ứng dụng...")
                # Quit app với exit code reload
                app = QApplication.instance()
                if app:
                    app.exit(EXIT_CODE_RELOAD)
                return
            self._stop_event.wait(self.interval)
    
    def stop(self):
        self._stop_event.set()


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
    
    # Khởi động File Watcher (hot-reload)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    watcher = FileWatcher(base_dir)
    watcher.start()
    
    # Import và tạo cửa sổ chính
    from frontend.main_window import MainWindow
    window = MainWindow()
    window.show()
    
    # Chạy event loop
    exit_code = app.exec_()
    
    # Dừng watcher
    watcher.stop()
    
    # Cleanup
    single_instance.cleanup()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

