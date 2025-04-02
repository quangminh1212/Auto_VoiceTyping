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
        self.timer.start(10)  # Kiểm tra mỗi 10ms
        self.last_ctrl_state = False

    def type_text(self, text):
        QTimer.singleShot(100, lambda: self._type_text(text))

    def _type_text(self, text):
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        print(f"Đã nhập văn bản: {text}")
        time.sleep(0.1)

    def check_ctrl_state(self):
        is_pressed = keyboard.is_pressed('ctrl')
        if is_pressed != self.last_ctrl_state:
            self.last_ctrl_state = is_pressed
            self.ctrl_pressed.emit(is_pressed)

