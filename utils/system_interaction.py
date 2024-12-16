import pyperclip
import speech_recognition as sr
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

class SystemInteraction:
    def __init__(self):
        self.current_device = None
        
    def get_audio_devices(self):
        try:
            mic = sr.Microphone()
            return mic.list_microphone_names()
        except Exception as e:
            print(f"Lỗi lấy danh sách microphone: {str(e)}")
            return []
        
    def get_current_device(self):
        return self.current_device
        
    def paste_text(self, text):
        try:
            if text and text.strip():
                # Lưu text vào clipboard
                pyperclip.copy(text)
                print(f"Đã copy text vào clipboard: [{text}]")
                
                # Giả lập Ctrl+V để paste
                app = QApplication.instance()
                if app:
                    clipboard = app.clipboard()
                    clipboard.setText(text)
                    print("Đã set text vào clipboard của Qt")
                
                return True
            else:
                print("Không có text để paste")
                return False
                
        except Exception as e:
            print(f"Lỗi khi paste text: {str(e)}")
            return False