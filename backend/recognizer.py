import os
import sys
from pydub import AudioSegment
import speech_recognition as sr
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import time
import warnings
import keyboard
from queue import Queue
import threading

# Tìm kiếm đường dẫn FFmpeg
def find_ffmpeg():
    # Các đường dẫn có thể có của FFmpeg
    possible_paths = [
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
        r"C:\Program Files (x86)\ffmpeg\bin",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ffmpeg", "bin"),
    ]
    
    # Kiểm tra nếu ffmpeg đã có trong PATH
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(path, "ffmpeg.exe")):
            return path
    
    # Kiểm tra các đường dẫn phổ biến
    for path in possible_paths:
        if os.path.exists(os.path.join(path, "ffmpeg.exe")):
            return path
            
    return None

# Tìm và cấu hình FFmpeg
ffmpeg_path = find_ffmpeg()

if ffmpeg_path:
    # Thêm đường dẫn FFmpeg vào PATH
    if ffmpeg_path not in os.environ["PATH"]:
        os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]
    
    # Cấu hình pydub
    AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
    AudioSegment.ffmpeg = os.path.join(ffmpeg_path, "ffmpeg.exe")
    AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")
    
    print(f"Đã tìm thấy FFmpeg tại: {ffmpeg_path}")
else:
    print("CẢNH BÁO: Không tìm thấy FFmpeg. Chức năng nhận dạng giọng nói có thể không hoạt động.")
    print("Vui lòng cài đặt FFmpeg và thêm vào PATH hoặc đặt vào thư mục C:\\ffmpeg\\bin")

# Tắt cảnh báo từ pydub
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pydub.utils")

class SpeechRecognizer(QObject):
    text_recognized = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.thread = None

    def start_listening(self):
        if not self.is_listening:
            if not ffmpeg_path:
                self.error_occurred.emit("Không tìm thấy FFmpeg. Vui lòng cài đặt FFmpeg để sử dụng chức năng nhận dạng giọng nói.")
                return
                
            self.is_listening = True
            self.thread = ListeningThread(self)
            self.thread.start()

    def stop_listening(self):
        if self.is_listening:
            self.is_listening = False
            if self.thread:
                self.thread.wait()

    def cleanup(self):
        self.stop_listening()

    def is_ctrl_pressed(self):
        return keyboard.is_pressed('ctrl')

class ListeningThread(QThread):
    def __init__(self, recognizer):
        super().__init__()
        self.recognizer = recognizer
        self.audio_queue = Queue()
        self.processing_thread = threading.Thread(target=self.process_audio_queue)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def run(self):
        start_time = time.time()
        total_duration = 0
        try:
            with sr.Microphone() as source:
                print("Đã khởi tạo Microphone thành công")
                self.recognizer.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                self.recognizer.recognizer.dynamic_energy_threshold = True
                self.recognizer.recognizer.energy_threshold = 300
                self.recognizer.recognizer.pause_threshold = 0.8
                
                while self.recognizer.is_listening:
                    try:
                        print("Đang lắng nghe...")
                        audio = self.recognizer.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        self.audio_queue.put(audio)
                    except sr.WaitTimeoutError:
                        print("Hết thời gian chờ, tiếp tục lắng nghe...")
                    except Exception as e:
                        print(f"Lỗi khi lắng nghe: {e}")
                        self.recognizer.error_occurred.emit(f"Lỗi khi lắng nghe: {e}")
                    time.sleep(0.05)
        except Exception as e:
            print(f"Lỗi khi khởi tạo microphone: {e}")
            self.recognizer.error_occurred.emit(f"Lỗi khi khởi tạo microphone: {e}")

    def process_audio_queue(self):
        while True:
            audio = self.audio_queue.get()
            self.process_audio(audio)
            self.audio_queue.task_done()

    def process_audio(self, audio):
        print("Đang xử lý âm thanh...")
        try:
            text = self.recognizer.recognizer.recognize_google(audio, language="vi-VN")
            print(f"Văn bản nhận diện: {text}")
            self.recognizer.text_recognized.emit(text)
        except sr.UnknownValueError:
            print("Không thể nhận diện giọng nói")
        except sr.RequestError as e:
            error_msg = f"Lỗi khi yêu cầu kết quả từ Google Speech Recognition: {e}"
            print(error_msg)
            self.recognizer.error_occurred.emit(error_msg)
        except Exception as e:
            error_msg = f"Lỗi không xác định khi xử lý âm thanh: {e}"
            print(error_msg)
            self.recognizer.error_occurred.emit(error_msg)

