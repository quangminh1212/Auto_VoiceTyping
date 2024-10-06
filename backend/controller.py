import pyautogui
import time
import pyperclip
import keyboard
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class InputController(QObject):
    ctrl_pressed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_ctrl_state)
        self.timer.start(100)  # Kiểm tra mỗi 100ms

    def type_text(self, text):
        # Sử dụng clipboard để nhập văn bản Unicode
        pyperclip.copy(text)
        
        # Nhấp chuột vào vị trí hiện tại
        current_position = pyautogui.position()
        pyautogui.click(current_position)
        
        # Dán văn bản từ clipboard
        pyautogui.hotkey('ctrl', 'v')
        
        # Đợi một chút để đảm bảo văn bản được dán hoàn toàn
        time.sleep(0.1)
        
        print(f"Đã nhập văn bản: {text}")

    def check_ctrl_state(self):
        is_pressed = keyboard.is_pressed('ctrl')
        self.ctrl_pressed.emit(is_pressed)
