import pyautogui
import time
import pyperclip

class InputController:
    def __init__(self):
        pass

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
