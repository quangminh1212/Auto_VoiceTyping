import pyautogui
import keyboard

class SystemInteraction:
    def __init__(self):
        pass
    
    def paste_text(self, text):
        pyautogui.write(text)

    def copy_text(self):
        pyautogui.hotkey('ctrl', 'c')
        return pyautogui.paste()

    def set_global_hotkey(self, hotkey, callback):
        keyboard.add_hotkey(hotkey, callback)

    def remove_global_hotkey(self, hotkey):
        keyboard.remove_hotkey(hotkey)