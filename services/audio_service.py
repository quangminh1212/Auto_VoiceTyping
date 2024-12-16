import speech_recognition as sr
import threading
import time
import pyaudio

class AudioService:
    def __init__(self):
        try:
            # Khởi tạo PyAudio để kiểm tra microphone
            p = pyaudio.PyAudio()
            device_info = p.get_default_input_device_info()
            print(f"\nMicrophone mặc định: {device_info['name']}")
            p.terminate()
            
            # Khởi tạo recognizer
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Test microphone
            with self.microphone as source:
                print("Kiểm tra microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Microphone hoạt động tốt!")
                
        except Exception as e:
            print(f"Lỗi khởi tạo audio: {str(e)}")
            raise
            
        self.is_recording = False
        self.current_text = ""
        self.recording_thread = None

    def _record_audio(self):
        with self.microphone as source:
            print("\n=== BẮT ĐẦU LẮNG NGHE ===")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while self.is_recording:
                try:
                    print("\nĐang lắng nghe... (Nói gì đó)")
                    audio = self.recognizer.listen(source, timeout=3)
                    print("Đã thu âm, đang xử lý...")
                    
                    try:
                        text = self.recognizer.recognize_google(audio, language='vi-VN')
                        print(f"Đã nhận dạng: [{text}]")
                        self.current_text = text  # Lưu text mới nhất
                        
                    except sr.UnknownValueError:
                        print("Không nhận dạng được giọng nói")
                    except sr.RequestError as e:
                        print(f"Lỗi API: {str(e)}")
                        
                except sr.WaitTimeoutError:
                    print("Hết thời gian chờ - tiếp tục lắng nghe")
                except Exception as e:
                    print(f"Lỗi ghi âm: {str(e)}")
                    time.sleep(0.5)

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
        if self.is_recording:
            print("\n=== DỪNG GHI ÂM ===")
            self.is_recording = False
            if self.recording_thread:
                self.recording_thread.join(timeout=2)
            return self.current_text
        return ""

    def get_current_text(self):
        return self.current_text

    def clear_text(self):
        self.current_text = ""
  