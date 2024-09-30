import speech_recognition as sr

class TextManager:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def speech_to_text(self, audio_file):
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio, language="vi-VN")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition không thể hiểu âm thanh")
            return None
        except sr.RequestError as e:
            print(f"Không thể yêu cầu kết quả từ Google Speech Recognition service; {e}")
            return None

    def process_text(self, text):
        # Xử lý văn bản nếu cần (ví dụ: loại bỏ khoảng trắng thừa, sửa lỗi chính tả, v.v.)
        return text.strip()