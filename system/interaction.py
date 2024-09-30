import pyautogui

class SystemInteraction:
    def __init__(self):
        pass
    
    def paste_text(self, text):
        current_position = pyautogui.position()
        pyautogui.click(current_position)
        pyautogui.hotkey('ctrl', 'v')