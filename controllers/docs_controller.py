from services.audio_service import AudioService

class DocsController:
    def __init__(self):
        self.audio_service = AudioService()
        self.current_text = ""
        
    def start_voice_typing(self):
        print("=== BẮT ĐẦU GHI ÂM ===")
        return self.audio_service.start_recording()
            
    def stop_voice_typing(self):
        print("=== DỪNG GHI ÂM ===")
        text = self.audio_service.stop_recording()
        if text:
            self.current_text = text
            print(f"Text đã ghi được: [{text}]")
        return self.current_text
        
    def get_text(self):
        text = self.audio_service.get_current_text()
        if not text:
            text = self.current_text
        return text

    def clear_text(self):
        self.current_text = ""
        self.audio_service.clear_text()