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

        # Điều chỉnh các thông số để tăng độ nhạy
        self.recognizer.energy_threshold = 300  # Giảm ngưỡng để dễ nhận diện hơn
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.3
        self.recognizer.phrase_threshold = 0.1
        self.recognizer.non_speaking_duration = 0.1

    def _record_audio(self):
        try:
            with self.microphone as source:
                print("Điều chỉnh nhiễu môi trường trong 2s...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("Đã điều chỉnh xong - Bắt đầu nghe...")
                
                while self.is_recording:
                    try:
                        print("Đang lắng nghe (nói gì đó vào mic)...")
                        audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)
                        print("Đã thu âm, đang xử lý...")
                        
                        # Thử nhận dạng với nhiều ngôn ngữ
                        for lang in ['vi-VN', 'en-US']:
                            try:
                                text = self.recognizer.recognize_google(audio, language=lang)
                                print(f"Đã nhận dạng được ({lang}): [{text}]")
                                self.current_text += text + " "
                                print(f"Text tích lũy: [{self.current_text}]")
                                break
                            except:
                                continue
                                
                    except sr.WaitTimeoutError:
                        print("Không nghe thấy gì - đang tiếp tục...")
                        continue
                    except sr.UnknownValueError:
                        print("Không nhận dạng được - thử lại...")
                        continue
                    except Exception as e:
                        print(f"Lỗi xử lý âm thanh: {str(e)}")
                        time.sleep(0.1)  # Tránh loop quá nhanh
                        continue
                        
        except Exception as e:
            print(f"Lỗi microphone: {str(e)}")
        finally:
            print("Kết thúc ghi âm")
            self.is_recording = False

    def start_recording(self):
        if not self.is_recording:
            self.current_text = ""  # Reset text
            self.is_recording = True
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.daemon = True  # Đảm bảo thread sẽ dừng khi chương trình dừng
            self.recording_thread.start()
            print("Đã bắt đầu thread ghi âm")

    def stop_recording(self):
        print("Đang dừng ghi âm...")
        self.is_recording = False
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=2)  # Đợi tối đa 2s
        final_text = self.current_text.strip()
        print(f"Text cuối cùng: [{final_text}]")
        return final_text

    def get_current_text(self):
        return self.current_text.strip()

    def clear_text(self):
        self.current_text = ""
  