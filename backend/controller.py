import pyautogui

class InputController:
    def __init__(self):
        pass

    def type_text(self, text):
        current_position = pyautogui.position()
        pyautogui.click(current_position)
        pyautogui.typewrite(text)
        print(f"Đã nhập văn bản: {text}")
