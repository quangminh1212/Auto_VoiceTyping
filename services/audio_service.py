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

        # Tăng các thông số nhận dạng
        self.recognizer.energy_threshold = 1000  # Giảm ngưỡng năng lượng để dễ nhận diện hơn
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5  # Giảm thời gian pause
        self.recognizer.phrase_threshold = 0.3  # Giảm ngưỡng phrase
        self.recognizer.non_speaking_duration = 0.3  # Giảm thời gian non-speaking

    def _record_audio(self):
        try:
            with self.microphone as source:
                print("Đang điều chỉnh nhiễu môi trường...")
                # Tăng thời gian điều chỉnh nhiễu
                self.recognizer.adjust_for_ambient_noise(source, duration=3)
                print("Đã điều chỉnh xong - Bắt đầu nghe...")
                
                while self.is_recording:
                    try:
                        print("Đang lắng nghe...")
                        # Giảm timeout và phrase_time_limit để nhận diện nhanh hơn
                        audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)
                        print("Đã nghe thấy - Đang xử lý...")
                        
                        # Thử nhận dạng với cả 2 ngôn ngữ
                        try:
                            text = self.recognizer.recognize_google(audio, language='vi-VN')
                        except:
                            text = self.recognizer.recognize_google(audio, language='en-US')
                            
                        print(f"Đã nhận dạng được: [{text}]")
                        
                        if text:
                            self.current_text += text + " "
                            print(f"Text hiện tại: [{self.current_text}]")
                            
                    except sr.WaitTimeoutError:
                        print("Không nghe thấy gì - tiếp tục nghe...")
                        continue
                    except sr.UnknownValueError:
                        print("Không nhận dạng được - thử lại...")
                        continue
                    except Exception as e:
                        print(f"Lỗi khi xử lý âm thanh: {str(e)}")
                        continue
                        
        except Exception as e:
            print(f"Lỗi microphone: {str(e)}")
        finally:
            print("Kết thúc ghi âm")
            self.is_recording = False

    def start_recording(self):
        if not self.is_recording:
            # Reset text khi bắt đầu ghi âm mới
            self.current_text = ""
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
  