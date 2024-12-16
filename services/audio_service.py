import speech_recognition as sr
import threading
import time

class AudioService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Chọn microphone mặc định
        try:
            self.microphone = sr.Microphone(device_index=None)
            print(f"Danh sách microphone: {sr.Microphone.list_microphone_names()}")
        except Exception as e:
            print(f"Lỗi khởi tạo microphone: {str(e)}")
        
        self.is_recording = False
        self.current_text = ""
        self.recording_thread = None

        # Điều chỉnh các thông số nhận dạng
        self.recognizer.energy_threshold = 100  # Giảm ngưỡng xuống thấp nhất
        self.recognizer.dynamic_energy_threshold = False  # Tắt dynamic threshold
        self.recognizer.pause_threshold = 0.3  # Giảm thời gian pause
        self.recognizer.phrase_threshold = 0.1  # Giảm ngưỡng phrase
        self.recognizer.non_speaking_duration = 0.1  # Giảm thời gian non-speaking

    def _record_audio(self):
        try:
            with self.microphone as source:
                print("\n=== KHỞI TẠO MICROPHONE ===")
                print("Điều chỉnh nhiễu môi trường...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Đã điều chỉnh xong - Bắt đầu nghe...")
                
                while self.is_recording:
                    try:
                        print("\nĐang lắng nghe... (Hãy nói gì đó)")
                        audio = self.recognizer.listen(source, 
                                                     timeout=2,
                                                     phrase_time_limit=5)
                        print("Đã thu âm, đang xử lý...")
                        
                        # Thử nhận dạng với cả tiếng Việt và tiếng Anh
                        text = None
                        for lang in ['vi-VN', 'en-US']:
                            try:
                                text = self.recognizer.recognize_google(audio, language=lang)
                                print(f"Đã nhận dạng được ({lang}): [{text}]")
                                break
                            except sr.UnknownValueError:
                                print(f"Không nhận dạng được với {lang}")
                                continue
                            except Exception as e:
                                print(f"Lỗi nhận dạng với {lang}: {str(e)}")
                                continue
                                
                        if text:
                            self.current_text += text + " "
                            print(f"Text tích lũy: [{self.current_text}]")
                        else:
                            print("Không nhận dạng được giọng nói, thử lại...")
                            
                    except sr.WaitTimeoutError:
                        print("Không nghe thấy gì - đang tiếp tục...")
                        continue
                    except Exception as e:
                        print(f"Lỗi trong quá trình ghi âm: {str(e)}")
                        time.sleep(0.1)
                        continue
                        
        except Exception as e:
            print(f"Lỗi critical với microphone: {str(e)}")
        finally:
            print("\n=== KẾT THÚC GHI ÂM ===")
            self.is_recording = False

    def start_recording(self):
        if not self.is_recording:
            print("\n=== BẮT ĐẦU PHIÊN GHI ÂM MỚI ===")
            self.current_text = ""  # Reset text
            self.is_recording = True
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            return True
        return False

    def stop_recording(self):
        print("\n=== DỪNG GHI ÂM ===")
        self.is_recording = False
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=2)
        final_text = self.current_text.strip()
        print(f"Text cuối cùng: [{final_text}]")
        return final_text

    def get_current_text(self):
        return self.current_text.strip()

    def clear_text(self):
        self.current_text = ""
  