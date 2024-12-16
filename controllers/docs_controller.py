from services.audio_service import AudioService

class DocsController:
    def __init__(self):
        self.audio_service = AudioService()
        self.current_text = ""
        
    def start_voice_typing(self):
        print("Bắt đầu ghi âm...")
        self.audio_service.start_recording()
            
    def stop_voice_typing(self):
        print("Dừng ghi âm...")
        text = self.audio_service.stop_recording()
        if text:
            self.current_text = text
        return self.current_text
        
    def get_text(self):
        return self.audio_service.get_current_text()

    def clear_text(self):
        self.audio_service.clear_text()
        self.current_text = ""