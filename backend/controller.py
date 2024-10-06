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
        # Sử dụng pyperclip để copy văn bản vào clipboard
        pyperclip.copy(text)
        # Sử dụng pyautogui để mô phỏng tổ hợp phím Ctrl+V
        pyautogui.hotkey('ctrl', 'v')
        print(f"Đã nhập văn bản: {text}")

    def check_ctrl_state(self):
        is_pressed = keyboard.is_pressed('ctrl')
        self.ctrl_pressed.emit(is_pressed)
