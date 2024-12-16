from services.audio_service import AudioService
from services.text_service import TextService

class DocsController:
    def __init__(self):
        self.audio_service = AudioService()
        self.text_service = TextService()
        self.current_text = ""
        
    def start_voice_typing(self):
        text = self.audio_service.start_recording()
        if text:
            self.current_text = text
            
    def stop_voice_typing(self):
        self.audio_service.stop_recording()
        
    def get_text(self):
        return self.current_text