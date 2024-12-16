import speech_recognition as sr
import threading
import time
import pyaudio

class AudioService:
    def __init__(self):
        try:
            # Kiểm tra và in thông tin audio
            audio = pyaudio.PyAudio()
            print("\n=== THÔNG TIN AUDIO SYSTEM ===")
            for i in range(audio.get_device_count()):
                device_info = audio.get_device_info_by_index(i)
                print(f"Device {i}: {device_info['name']}")
                print(f"- Input channels: {device_info['maxInputChannels']}")
                print(f"- Default Sample Rate: {device_info['defaultSampleRate']}")
            
            # Tìm default input device
            default_input = audio.get_default_input_device_info()
            print(f"\nDefault Input Device: {default_input['name']}")
            
            # Khởi tạo recognizer với các thông số cụ thể
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 100
            self.recognizer.dynamic_energy_threshold = False
            self.recognizer.pause_threshold = 0.3
            self.recognizer.phrase_threshold = 0.1
            self.recognizer.non_speaking_duration = 0.1

            # Khởi tạo microphone với device index cụ thể
            device_index = None
            for i in range(audio.get_device_count()):
                if audio.get_device_info_by_index(i)['maxInputChannels'] > 0:
                    device_index = i
                    break
            
            self.microphone = sr.Microphone(device_index=device_index)
            print(f"Đã chọn microphone index: {device_index}")
            
            # Test microphone
            with self.microphone as source:
                print("\nTest thu âm 1 giây...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Microphone hoạt động tốt!")
                
        except Exception as e:
            print(f"Lỗi khởi tạo audio system: {str(e)}")
            raise
            
        self.is_recording = False
        self.current_text = ""
        self.recording_thread = None

    def _record_audio(self):
        try:
            with self.microphone as source:
                print("\n=== BẮT ĐẦU GHI ÂM ===")
                print("Điều chỉnh nhiễu trong 2 giây...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print(f"Mức năng lượng hiện tại: {self.recognizer.energy_threshold}")
                
                while self.is_recording:
                    try:
                        print("\nĐang lắng nghe... (Nói to và rõ ràng)")
                        audio = self.recognizer.listen(source, 
                                                     timeout=2,
                                                     phrase_time_limit=5)
                        print("Đã thu được âm thanh, đang xử lý...")
                        
                        # Thử với nhiều cài đặt khác nhau
                        text = None
                        for lang in ['vi-VN', 'en-US']:
                            try:
                                text = self.recognizer.recognize_google(
                                    audio, 
                                    language=lang,
                                    show_all=True  # Hiển thị tất cả kết quả có thể
                                )
                                if text:
                                    if isinstance(text, dict):
                                        # Lấy kết quả có confidence cao nhất
                                        text = text.get('alternative', [{}])[0].get('transcript', '')
                                    print(f"Đã nhận dạng ({lang}): [{text}]")
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
                            print("Không nhận dạng được, thử lại...")
                            
                    except sr.WaitTimeoutError:
                        print("Hết thời gian chờ - tiếp tục lắng nghe...")
                        continue
                    except Exception as e:
                        print(f"Lỗi ghi âm: {str(e)}")
                        time.sleep(0.1)
                        continue
                        
        except Exception as e:
            print(f"Lỗi critical: {str(e)}")
        finally:
            print("\n=== KẾT THÚC GHI ÂM ===")
            self.is_recording = False

    def start_recording(self):
        if not self.is_recording:
            print("\n=== KHỞI TẠO PHIÊN GHI ÂM MỚI ===")
            self.current_text = ""
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
  