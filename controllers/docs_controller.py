from services.audio_service import AudioService

class DocsController:
    def __init__(self):
        self.audio_service = AudioService()
        self.current_text = ""
        
    def start_voice_typing(self):
        try:
            print("Khởi tạo ghi âm...")
            self.audio_service.start_recording()
            return True
        except Exception as e:
            print(f"Lỗi khi bắt đầu ghi âm: {str(e)}")
            return False
            
    def stop_voice_typing(self):
        try:
            print("Đang dừng và lấy text...")
            text = self.audio_service.stop_recording()
            if text:
                self.current_text = text
                print(f"Đã nhận được text: [{self.current_text}]")
            return self.current_text
        except Exception as e:
            print(f"Lỗi khi dừng ghi âm: {str(e)}")
            return ""
        
    def get_text(self):
        try:
            text = self.audio_service.get_current_text()
            if not text:  # Nếu không có text mới, trả về text đã lưu
                text = self.current_text
            print(f"Lấy text hiện tại: [{text}]")
            return text
        except Exception as e:
            print(f"Lỗi khi lấy text: {str(e)}")
            return self.current_text

    def clear_text(self):
        self.audio_service.clear_text()
        self.current_text = ""