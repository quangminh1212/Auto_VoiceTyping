import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize_speech(self):
        with sr.Microphone() as source:
            print("Đang lắng nghe...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language="vi-VN")
            print(f"Đã nhận diện: {text}")
            return text
        except sr.UnknownValueError:
            print("Không thể nhận diện giọng nói")
        except sr.RequestError as e:
            print(f"Lỗi khi yêu cầu kết quả từ Google Speech Recognition; {e}")
        return None
