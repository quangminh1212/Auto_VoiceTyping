import pyperclip
import speech_recognition as sr
from PyQt6.QtWidgets import QApplication
import win32clipboard
import win32con
import time

class SystemInteraction:
    def __init__(self):
        self.current_device = None
        
    def get_audio_devices(self):
        try:
            mic = sr.Microphone()
            return mic.list_microphone_names()
        except Exception as e:
            print(f"Lỗi lấy danh sách microphone: {str(e)}")
            return ["Default"]
        
    def get_current_device(self):
        return self.current_device
        
    def paste_text(self, text):
        if not text:
            print("Không có text để paste")
            return False
            
        try:
            # Phương thức 1: Sử dụng pyperclip
            pyperclip.copy(text)
            print(f"Đã copy vào clipboard (pyperclip): [{text}]")
            
            # Phương thức 2: Sử dụng win32clipboard
            self.set_clipboard_text(text)
            print(f"Đã copy vào clipboard (win32): [{text}]")
            
            # Phương thức 3: Sử dụng Qt clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            print(f"Đã copy vào clipboard (Qt): [{text}]")
            
            # Verify clipboard content
            verify_text = pyperclip.paste()
            if verify_text == text:
                print("Xác nhận text đã được copy thành công")
                return True
            else:
                print(f"Text trong clipboard khác với text gốc: [{verify_text}]")
                return False
                
        except Exception as e:
            print(f"Lỗi khi paste text: {str(e)}")
            return False
            
    def set_clipboard_text(self, text):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
        except Exception as e:
            print(f"Lỗi win32clipboard: {str(e)}")