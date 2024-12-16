import pyperclip
import speech_recognition as sr

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
            if text:
                pyperclip.copy(text)
                print(f"Đã copy text: {text}")
                return True
        except Exception as e:
            print(f"Lỗi khi paste text: {str(e)}")
            return False