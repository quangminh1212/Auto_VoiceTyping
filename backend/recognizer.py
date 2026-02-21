"""
Voice Recognition Engine - Always-on Microphone Architecture
Microphone luôn mở sẵn, chỉ toggle thu/xử lý khi Alt nhấn
Tối ưu cho tiếng Việt với Google Speech API
"""

import warnings
import time
import threading
from queue import Queue, Empty
from enum import Enum

import numpy as np
import speech_recognition as sr
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import keyboard

# Tắt cảnh báo
warnings.filterwarnings("ignore")


class RecognitionEngine(Enum):
    """Enum cho các engine nhận dạng có hỗ trợ"""
    GOOGLE = "google"
    WHISPER = "whisper"
    FASTER_WHISPER = "faster_whisper"


class SpeechRecognizer(QObject):
    """
    Speech Recognizer với Always-On Microphone Architecture
    - Mic mở sẵn, calibrate 1 lần duy nhất
    - Toggle listening gần như tức thì (< 50ms)
    - Tối ưu parameters cho tiếng Việt
    """
    # Signals
    text_recognized = pyqtSignal(str)
    status_changed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    audio_level = pyqtSignal(float)
    listening_started = pyqtSignal()
    listening_stopped = pyqtSignal()

    def __init__(self, engine=RecognitionEngine.GOOGLE, language="vi-VN"):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self._is_running = False  # Thread chính đang chạy
        self._thread = None
        self.engine = engine
        self.language = language
        
        # Cấu hình recognizer tối ưu cho tiếng Việt
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 250       # Nhạy hơn để bắt giọng nói nhẹ
        self.recognizer.pause_threshold = 1.0         # Tiếng Việt cần pause dài hơn (tránh cắt giữa câu)
        self.recognizer.phrase_threshold = 0.2        # Nhận phrase nhanh hơn
        self.recognizer.non_speaking_duration = 0.4   # Thời gian im lặng trước khi dừng
        self.recognizer.operation_timeout = None      # Không timeout operation

    def set_engine(self, engine: RecognitionEngine):
        """Đổi engine nhận dạng"""
        self.engine = engine
        self.status_changed.emit(f"Đã chuyển sang engine: {engine.value}")

    def set_language(self, language: str):
        """Đổi ngôn ngữ nhận dạng"""
        self.language = language
        
        # Tối ưu params theo ngôn ngữ
        if "vi" in language.lower():
            self.recognizer.pause_threshold = 1.0
            self.recognizer.phrase_threshold = 0.2
            self.recognizer.non_speaking_duration = 0.4
        else:
            self.recognizer.pause_threshold = 0.8
            self.recognizer.phrase_threshold = 0.3
            self.recognizer.non_speaking_duration = 0.5
        
        lang_name = "Tiếng Việt" if "vi" in language.lower() else "English"
        self.status_changed.emit(f"Ngôn ngữ: {lang_name}")

    def initialize(self):
        """Khởi tạo microphone thread (gọi 1 lần khi app start)"""
        if self._is_running:
            return
        self._is_running = True
        self._thread = AlwaysOnMicThread(self)
        self._thread.start()

    def start_listening(self):
        """Bắt đầu lắng nghe - gần như tức thì vì mic đã mở sẵn"""
        if not self._is_running:
            self.initialize()
        
        if not self.is_listening:
            self.is_listening = True
            self.listening_started.emit()
            self.status_changed.emit("Đang lắng nghe...")

    def stop_listening(self):
        """Dừng lắng nghe - chỉ set flag, không đóng mic"""
        if self.is_listening:
            self.is_listening = False
            self.listening_stopped.emit()
            self.status_changed.emit("Sẵn sàng")

    def cleanup(self):
        """Dọn dẹp tài nguyên - đóng mic và thread"""
        self.is_listening = False
        self._is_running = False
        if self._thread:
            self._thread.wait(3000)

    def is_alt_pressed(self):
        """Kiểm tra phím Alt có đang được nhấn"""
        return keyboard.is_pressed('alt')


class AlwaysOnMicThread(QThread):
    """
    Thread giữ microphone luôn mở. 
    - Calibrate 1 lần duy nhất khi khởi tạo
    - Khi is_listening=True → thu và xử lý audio
    - Khi is_listening=False → chỉ đọc audio level (không xử lý)
    """
    
    def __init__(self, recognizer: SpeechRecognizer):
        super().__init__()
        self.recognizer = recognizer
        self.audio_queue = Queue()
        self._processing_thread = None

    def run(self):
        """Main thread - giữ mic mở liên tục"""
        # Start processing thread
        self._processing_thread = threading.Thread(
            target=self._process_audio_loop,
            daemon=True
        )
        self._processing_thread.start()

        try:
            with sr.Microphone(sample_rate=16000) as source:
                # Calibrate 1 lần duy nhất
                self.recognizer.status_changed.emit("Đang hiệu chỉnh micro...")
                self.recognizer.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                self.recognizer.status_changed.emit("Sẵn sàng")

                while self.recognizer._is_running:
                    if self.recognizer.is_listening:
                        try:
                            # Thu audio với timeout ngắn để responsive
                            audio = self.recognizer.recognizer.listen(
                                source,
                                timeout=3,
                                phrase_time_limit=30  # Cho phép câu dài hơn cho tiếng Việt
                            )

                            # Tính audio level từ raw data
                            self._emit_audio_level(audio)

                            # Kiểm tra lại trước khi đưa vào queue
                            if self.recognizer.is_listening:
                                self.audio_queue.put(audio)

                        except sr.WaitTimeoutError:
                            self.recognizer.audio_level.emit(0.0)
                            continue
                        except Exception as e:
                            if self.recognizer._is_running:
                                self.recognizer.error_occurred.emit(f"Lỗi thu âm: {str(e)}")
                    else:
                        # Mic vẫn mở nhưng không thu - sleep ngắn để không chiếm CPU
                        time.sleep(0.05)

        except Exception as e:
            if self.recognizer._is_running:
                self.recognizer.error_occurred.emit(f"Lỗi microphone: {str(e)}")

    def _emit_audio_level(self, audio):
        """Tính và emit audio level"""
        try:
            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
            if len(audio_data) > 0:
                level = np.abs(audio_data).mean() / 32768.0
                self.recognizer.audio_level.emit(min(level * 3, 1.0))
        except Exception:
            pass

    def _process_audio_loop(self):
        """Background thread xử lý queue audio"""
        while self.recognizer._is_running:
            try:
                audio = self.audio_queue.get(timeout=1)
                self._recognize_audio(audio)
                self.audio_queue.task_done()
            except Empty:
                continue
            except Exception:
                continue

    def _recognize_audio(self, audio):
        """Nhận dạng giọng nói từ audio"""
        self.recognizer.status_changed.emit("Đang xử lý...")

        try:
            # Nhận dạng với Google Speech API
            text = self.recognizer.recognizer.recognize_google(
                audio,
                language=self.recognizer.language,
                show_all=False
            )

            if text and text.strip():
                print(f"[Nhận dạng] {text}")
                self.recognizer.text_recognized.emit(text.strip())
                if self.recognizer.is_listening:
                    self.recognizer.status_changed.emit("Đang lắng nghe...")
                else:
                    self.recognizer.status_changed.emit("Sẵn sàng")
            else:
                if self.recognizer.is_listening:
                    self.recognizer.status_changed.emit("Đang lắng nghe...")

        except sr.UnknownValueError:
            # Không nhận dạng được - bình thường
            if self.recognizer.is_listening:
                self.recognizer.status_changed.emit("Đang lắng nghe...")
        except sr.RequestError as e:
            self.recognizer.error_occurred.emit(f"Lỗi API: {str(e)}")
        except Exception as e:
            self.recognizer.error_occurred.emit(f"Lỗi: {str(e)}")
