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
        # Điều chỉnh các thông số nhận dạng
        self.recognizer.energy_threshold = 4000  # Tăng độ nhạy
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # Giảm thời gian pause

    def _record_audio(self):
        try:
            with self.microphone as source:
                print("Điều chỉnh độ ồn môi trường...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("Bắt đầu ghi âm - Hãy nói...")
                
                while self.is_recording:
                    try:
                        print("Đang lắng nghe...")
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        print("Đang xử lý âm thanh...")
                        
                        text = self.recognizer.recognize_google(audio, language='vi-VN')
                        print(f"Đã nhận dạng: [{text}]")
                        
                        if text:
                            self.current_text += text + " "
                            print(f"Text hiện tại: [{self.current_text}]")
                            
                    except sr.WaitTimeoutError:
                        print("Timeout - không nghe thấy gì")
                        continue
                    except sr.UnknownValueError:
                        print("Không nhận dạng được giọng nói")
                        continue
                    except Exception as e:
                        print(f"Lỗi trong quá trình ghi âm: {str(e)}")
                        continue
                        
        except Exception as e:
            print(f"Lỗi khởi tạo microphone: {str(e)}")
        finally:
            print("Kết thúc ghi âm")
            self.is_recording = False

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.start()
            print("Đã bắt đầu thread ghi âm")

    def stop_recording(self):
        print("Đang dừng ghi âm...")
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join()
        final_text = self.current_text
        print(f"Text cuối cùng: [{final_text}]")
        return final_text

    def get_current_text(self):
        return self.current_text.strip()

    def clear_text(self):
        self.current_text = "" 