"""
Input Controller - Điều khiển nhập văn bản và phím tắt
"""

import pyautogui
import time
import pyperclip
import keyboard
from PyQt5.QtCore import QObject, pyqtSignal, QTimer


class InputController(QObject):
    """Controller xử lý phím tắt và nhập văn bản"""
    
    alt_pressed = pyqtSignal(bool)
    text_typed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_alt_state)
        self.timer.start(50)  # Kiểm tra mỗi 50ms
        self.last_alt_state = False
        self.pending_text = None
        
        # Cấu hình pyautogui
        pyautogui.PAUSE = 0.05
        pyautogui.FAILSAFE = False

    def type_text(self, text):
        """Nhập văn bản sau khi thả phím Alt"""
        if not text or not text.strip():
            return
            
        self.pending_text = text.strip()
        print(f"[Controller] Đã nhận văn bản: {text}")
        
        # Đợi người dùng thả Alt rồi mới paste
        QTimer.singleShot(200, self._check_and_type)

    def _check_and_type(self):
        """Kiểm tra và paste khi Alt đã thả"""
        if self.pending_text is None:
            return
            
        # Nếu Alt vẫn đang nhấn, chờ thêm
        if keyboard.is_pressed('alt'):
            QTimer.singleShot(100, self._check_and_type)
            return
        
        # Thực hiện paste
        self._do_paste(self.pending_text)
        self.pending_text = None

    def _do_paste(self, text):
        """Thực hiện paste văn bản"""
        try:
            # Thêm khoảng trắng trước nếu cần
            text_to_paste = text
            
            # Copy vào clipboard
            pyperclip.copy(text_to_paste)
            
            # Đợi một chút để đảm bảo clipboard ready
            time.sleep(0.05)
            
            # Paste
            pyautogui.hotkey('ctrl', 'v')
            
            # Thêm khoảng trắng sau
            time.sleep(0.05)
            pyautogui.press('space')
            
            print(f"[Controller] Đã paste: {text}")
            self.text_typed.emit(text)
            
        except Exception as e:
            print(f"[Controller] Lỗi paste: {e}")

    def check_alt_state(self):
        """Kiểm tra trạng thái phím Alt"""
        try:
            is_pressed = keyboard.is_pressed('alt')
            if is_pressed != self.last_alt_state:
                self.last_alt_state = is_pressed
                self.alt_pressed.emit(is_pressed)
                
                if is_pressed:
                    print("[Controller] Alt pressed - Start listening")
                else:
                    print("[Controller] Alt released - Stop listening")
        except Exception:
            pass
