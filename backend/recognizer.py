import speech_recognition as sr
from PyQt5.QtCore import QThread, pyqtSignal

class SpeechRecognizer(QThread):
    text_recognized = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        
    def run(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.energy_threshold = 4000
            
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, phrase_time_limit=10, timeout=None)
                    text = self.recognizer.recognize_google(audio, language="vi-VN", show_all=True)
                    if isinstance(text, dict) and 'alternative' in text:
                        best_result = text['alternative'][0]['transcript']
                        self.text_recognized.emit(best_result)
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"Lỗi khi yêu cầu kết quả từ Google Speech Recognition; {e}")

    def start_listening(self):
        self.is_listening = True
        self.start()

    def stop_listening(self):
        self.is_listening = False
