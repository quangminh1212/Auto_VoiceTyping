import pyperclip

class SystemInteraction:
    def __init__(self):
        self.current_device = None
        
    def get_audio_devices(self):
        # Implement get audio devices
        return ["Default"]
        
    def get_current_device(self):
        return self.current_device
        
    def paste_text(self, text):
        pyperclip.copy(text)