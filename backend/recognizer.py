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
import logging

# Chỉ định đường dẫn đến FFmpeg
ffmpeg_path = r"C:\ffmpeg\bin"

# Thêm đường dẫn FFmpeg vào PATH
if ffmpeg_path not in os.environ["PATH"]:
    os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]

# Cấu hình pydub
AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffmpeg = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")

# Kiểm tra xem FFmpeg có tồn tại không
if not os.path.exists(AudioSegment.converter):
    print(f"Không tìm thấy FFmpeg tại {AudioSegment.converter}")
    sys.exit(1)

# Tắt cảnh báo từ pydub
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pydub.utils")

logger = logging.getLogger(__name__)

class SpeechRecognizer(QObject):
    text_recognized = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.thread = None

    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.thread = ListeningThread(self)
            self.thread.start()

    def stop_listening(self):
        if self.is_listening:
            self.is_listening = False
            if self.thread:
                self.thread.wait()

    def cleanup(self):
        logger.info("Dọn dẹp tài nguyên...")
        self.stop_listening()
        logger.info("Đã dọn dẹp xong")

    def is_alt_pressed(self):
        return keyboard.is_pressed('alt')

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
        with sr.Microphone() as source:
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
                    print(f"Lỗi: {e}")
                time.sleep(0.05)

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
            print(f"Lỗi khi yêu cầu kết quả từ Google Speech Recognition; {e}")

