import speech_recognition as sr

class AudioService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_recording = False
        
    def start_recording(self):
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                self.is_recording = True
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio, language='vi-VN')
                return text
        except Exception as e:
            print(f"Lỗi ghi âm: {str(e)}")
            return None
            
    def stop_recording(self):
        self.is_recording = False 