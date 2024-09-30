import pyautogui

try:
    import keyboard
except ImportError:
    print("Không thể import keyboard. Hãy chắc chắn bạn đã cài đặt thư viện keyboard.")
    print("Chạy lệnh: pip install keyboard")
    keyboard = None

class SystemInteraction:
    def __init__(self):
        pass
    
    def paste_text(self, text):
        pyautogui.write(text)

    def copy_text(self):
        pyautogui.hotkey('ctrl', 'c')
        return pyautogui.paste()

    def set_global_hotkey(self, hotkey, callback):
        if keyboard:
            keyboard.add_hotkey(hotkey, callback)
        else:
            print("Không thể đặt phím tắt toàn cục do thiếu thư viện keyboard.")

    def remove_global_hotkey(self, hotkey):
        if keyboard:
            keyboard.remove_hotkey(hotkey)
        else:
            print("Không thể xóa phím tắt toàn cục do thiếu thư viện keyboard.")