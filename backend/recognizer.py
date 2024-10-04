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
            self.recognizer.adjust_for_ambient_noise(source)
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio, language="vi-VN")
                    self.text_recognized.emit(text)
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    print("Không thể nhận diện giọng nói")
                except sr.RequestError as e:
                    print(f"Lỗi khi yêu cầu kết quả từ Google Speech Recognition; {e}")

    def start_listening(self):
        self.is_listening = True
        self.start()

    def stop_listening(self):
        self.is_listening = False
