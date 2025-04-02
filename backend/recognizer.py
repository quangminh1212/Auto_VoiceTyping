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

# Cấu hình logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("voicetyping.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SpeechRecognizer")

# Tìm kiếm đường dẫn FFmpeg
def find_ffmpeg():
    # Các đường dẫn có thể có của FFmpeg
    possible_paths = [
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
        r"C:\Program Files (x86)\ffmpeg\bin",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ffmpeg", "bin"),
    ]
    
    logger.info("Đang tìm kiếm FFmpeg...")
    
    # Kiểm tra nếu ffmpeg đã có trong PATH
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(path, "ffmpeg.exe")):
            logger.info(f"Tìm thấy FFmpeg trong PATH tại: {path}")
            return path
    
    # Kiểm tra các đường dẫn phổ biến
    for path in possible_paths:
        if os.path.exists(os.path.join(path, "ffmpeg.exe")):
            logger.info(f"Tìm thấy FFmpeg tại đường dẫn phổ biến: {path}")
            return path
            
    logger.warning("Không tìm thấy FFmpeg trong bất kỳ đường dẫn nào")
    return None

# Tìm và cấu hình FFmpeg
ffmpeg_path = find_ffmpeg()

if ffmpeg_path:
    # Thêm đường dẫn FFmpeg vào PATH
    if ffmpeg_path not in os.environ["PATH"]:
        os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]
        logger.info(f"Đã thêm {ffmpeg_path} vào PATH")
    
    # Cấu hình pydub
    AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
    AudioSegment.ffmpeg = os.path.join(ffmpeg_path, "ffmpeg.exe")
    AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")
    
    logger.info(f"Đã cấu hình pydub với FFmpeg tại: {ffmpeg_path}")
else:
    logger.error("CẢNH BÁO: Không tìm thấy FFmpeg. Chức năng nhận dạng giọng nói sẽ không hoạt động.")
    logger.error("Vui lòng cài đặt FFmpeg và thêm vào PATH hoặc đặt vào một trong các thư mục:")
    for path in [r"C:\ffmpeg\bin", r"C:\Program Files\ffmpeg\bin", r"C:\Program Files (x86)\ffmpeg\bin"]:
        logger.error(f"  - {path}")

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
        logger.info("SpeechRecognizer khởi tạo")
        
        # Kiểm tra microphone
        self._check_microphones()

    def _check_microphones(self):
        try:
            mics = sr.Microphone.list_microphone_names()
            logger.info(f"Microphones có sẵn ({len(mics)}): {mics}")
            if not mics:
                logger.error("Không tìm thấy microphone nào. Vui lòng kết nối microphone và thử lại.")
                self.error_occurred.emit("Không tìm thấy microphone. Vui lòng kết nối và thử lại.")
        except Exception as e:
            logger.exception(f"Lỗi khi kiểm tra microphone: {e}")
            self.error_occurred.emit(f"Lỗi khi kiểm tra microphone: {e}")

    def start_listening(self):
        if not self.is_listening:
            if not ffmpeg_path:
                error_msg = "Không tìm thấy FFmpeg. Vui lòng cài đặt FFmpeg để sử dụng chức năng nhận dạng giọng nói."
                logger.error(error_msg)
                self.error_occurred.emit(error_msg)
                return
                
            logger.info("Bắt đầu lắng nghe...")
            self.is_listening = True
            self.thread = ListeningThread(self)
            self.thread.start()

    def stop_listening(self):
        if self.is_listening:
            logger.info("Dừng lắng nghe...")
            self.is_listening = False
            if self.thread:
                self.thread.wait()
                logger.info("Đã dừng thread lắng nghe")

    def cleanup(self):
        logger.info("Dọn dẹp tài nguyên...")
        self.stop_listening()
        logger.info("Đã dọn dẹp xong")

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
        logger.info("ListeningThread khởi tạo")

    def run(self):
        start_time = time.time()
        total_duration = 0
        try:
            logger.info("Đang khởi tạo Microphone...")
            with sr.Microphone() as source:
                logger.info("Đã khởi tạo Microphone thành công")
                logger.info("Đang điều chỉnh cho tiếng ồn môi trường...")
                self.recognizer.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                logger.info(f"Ngưỡng năng lượng: {self.recognizer.recognizer.energy_threshold}")
                
                self.recognizer.recognizer.dynamic_energy_threshold = True
                self.recognizer.recognizer.energy_threshold = 300
                self.recognizer.recognizer.pause_threshold = 0.8
                
                logger.info("Bắt đầu vòng lặp lắng nghe...")
                while self.recognizer.is_listening:
                    try:
                        logger.debug("Đang lắng nghe...")
                        audio = self.recognizer.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        logger.debug(f"Đã thu âm (thời lượng khoảng: {len(audio.frame_data)/audio.sample_rate:.2f}s)")
                        self.audio_queue.put(audio)
                    except sr.WaitTimeoutError:
                        logger.debug("Hết thời gian chờ, tiếp tục lắng nghe...")
                    except Exception as e:
                        logger.exception(f"Lỗi khi lắng nghe: {e}")
                        self.recognizer.error_occurred.emit(f"Lỗi khi lắng nghe: {e}")
                    time.sleep(0.05)
                logger.info("Đã thoát vòng lặp lắng nghe")
        except Exception as e:
            logger.exception(f"Lỗi khi khởi tạo microphone: {e}")
            self.recognizer.error_occurred.emit(f"Lỗi khi khởi tạo microphone: {e}")
        logger.info("ListeningThread đã kết thúc")

    def process_audio_queue(self):
        logger.info("Bắt đầu thread xử lý âm thanh")
        while True:
            try:
                audio = self.audio_queue.get()
                logger.debug("Đã lấy âm thanh từ hàng đợi để xử lý")
                self.process_audio(audio)
                self.audio_queue.task_done()
            except Exception as e:
                logger.exception(f"Lỗi trong vòng lặp xử lý âm thanh: {e}")

    def process_audio(self, audio):
        logger.info("Đang xử lý âm thanh và gửi đến Google Speech Recognition...")
        try:
            text = self.recognizer.recognizer.recognize_google(audio, language="vi-VN")
            logger.info(f"Văn bản nhận diện: '{text}'")
            self.recognizer.text_recognized.emit(text)
        except sr.UnknownValueError:
            logger.warning("Không thể nhận diện giọng nói (không có kết quả phù hợp)")
        except sr.RequestError as e:
            error_msg = f"Lỗi khi yêu cầu kết quả từ Google Speech Recognition: {e}"
            logger.error(error_msg)
            self.recognizer.error_occurred.emit(error_msg)
        except Exception as e:
            error_msg = f"Lỗi không xác định khi xử lý âm thanh: {e}"
            logger.exception(error_msg)
            self.recognizer.error_occurred.emit(error_msg)

