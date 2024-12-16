import speech_recognition as sr
import threading
import time

class AudioService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_recording = False
        self.current_text = ""
        self.recording_thread = None

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.start()

    def _record_audio(self):
        try:
            with self.microphone as source:
                print("Điều chỉnh độ ồn môi trường...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Đang ghi âm...")
                
                while self.is_recording:
                    try:
                        audio = self.recognizer.listen(source, timeout=5)
                        text = self.recognizer.recognize_google(audio, language='vi-VN')
                        print(f"Đã nhận dạng: {text}")
                        self.current_text += text + " "
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        print("Không nhận dạng được giọng nói")
                    except Exception as e:
                        print(f"Lỗi khi ghi âm: {str(e)}")
                        break
                        
        except Exception as e:
            print(f"Lỗi khởi tạo microphone: {str(e)}")
        finally:
            self.is_recording = False

    def stop_recording(self):
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join()
        return self.current_text

    def get_current_text(self):
        return self.current_text

    def clear_text(self):
        self.current_text = "" 