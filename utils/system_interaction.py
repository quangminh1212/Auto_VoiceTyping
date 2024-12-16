import pyperclip
import time
from PyQt6.QtWidgets import QApplication

class SystemInteraction:
    def __init__(self):
        self.current_device = None
        
    def get_audio_devices(self):
        try:
            import speech_recognition as sr
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
            # Thử nhiều cách paste
            # 1. Dùng pyperclip
            pyperclip.copy(text)
            time.sleep(0.1)  # Đợi clipboard cập nhật
            
            # 2. Dùng Qt clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            time.sleep(0.1)
            
            print(f"Đã copy text vào clipboard: [{text}]")
            return True
                
        except Exception as e:
            print(f"Lỗi khi paste text: {str(e)}")
            return False