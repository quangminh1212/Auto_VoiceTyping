import speech_recognition as sr
import threading
import time

class AudioService:
    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.is_recording = False
            self.current_text = ""
            self.recording_thread = None
            
            # Test PyAudio
            with self.microphone as source:
                print("Kiểm tra microphone thành công!")
                
        except Exception as e:
            print(f"Lỗi khởi tạo AudioService: {str(e)}")
            raise

    def _record_audio(self):
        with self.microphone as source:
            # Điều chỉnh nhiễu
            print("\nĐang điều chỉnh nhiễu môi trường...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Đã điều chỉnh xong!")

            while self.is_recording:
                try:
                    # Ghi âm
                    print("\nĐang lắng nghe (Hãy nói gì đó)...")
                    audio = self.recognizer.listen(source)
                    print("Đã ghi được âm thanh, đang xử lý...")

                    # Chuyển âm thanh thành văn bản
                    text = self.recognizer.recognize_google(audio, language='vi-VN')
                    print(f"Đã nhận dạng được: [{text}]")
                    self.current_text = text
                    
                except sr.UnknownValueError:
                    print("Không nhận dạng được giọng nói, hãy thử lại...")
                except sr.RequestError as e:
                    print(f"Lỗi kết nối Google API: {e}")
                except Exception as e:
                    print(f"Lỗi: {str(e)}")
                    time.sleep(0.5)

    def start_recording(self):
        try:
            print("\n=== BẮT ĐẦU GHI ÂM ===")
            self.current_text = ""
            self.is_recording = True
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.start()
            return True
        except Exception as e:
            print(f"Lỗi khi bắt đầu ghi âm: {str(e)}")
            return False

    def stop_recording(self):
        try:
            print("\n=== DỪNG GHI ÂM ===")
            self.is_recording = False
            if self.recording_thread:
                self.recording_thread.join()
            print(f"Text cuối cùng: [{self.current_text}]")
            return self.current_text
        except Exception as e:
            print(f"Lỗi khi dừng ghi âm: {str(e)}")
            return ""

    def get_current_text(self):
        return self.current_text
  