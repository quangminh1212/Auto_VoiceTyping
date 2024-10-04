import speech_recognition as sr
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import time

class SpeechRecognizer(QObject):
    text_recognized = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.thread = None

    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.thread = ListeningThread(self)
            self.thread.start()

    def stop_listening(self):
        if self.is_listening:
            self.is_listening = False
            if self.thread:
                self.thread.wait()

    def cleanup(self):
        self.stop_listening()

class ListeningThread(QThread):
    def __init__(self, recognizer):
        super().__init__()
        self.recognizer = recognizer

    def run(self):
        with self.recognizer.microphone as source:
            self.recognizer.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while self.recognizer.is_listening:
                try:
                    audio = self.recognizer.recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    text = self.recognizer.recognizer.recognize_google(audio, language="vi-VN")
                    self.recognizer.text_recognized.emit(text)
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    print("Không thể nhận diện giọng nói")
                except sr.RequestError as e:
                    print(f"Lỗi khi yêu cầu kết quả từ Google Speech Recognition; {e}")
                
                time.sleep(0.1)
