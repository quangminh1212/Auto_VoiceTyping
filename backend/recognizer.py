"""
Voice Recognition Engine - Sử dụng PyAudio + Google Speech API
"""

import warnings
import time
import threading
from queue import Queue
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
    Speech Recognizer sử dụng PyAudio + Google Speech API
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
        self.thread = None
        self.engine = engine
        self.language = language
        
        # Cấu hình recognizer tối ưu
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5

    def set_engine(self, engine: RecognitionEngine):
        """Đổi engine nhận dạng"""
        self.engine = engine
        self.status_changed.emit(f"Đã chuyển sang engine: {engine.value}")

    def set_language(self, language: str):
        """Đổi ngôn ngữ nhận dạng"""
        self.language = language
        lang_name = "Tiếng Việt" if "vi" in language.lower() else "English"
        self.status_changed.emit(f"Ngôn ngữ: {lang_name}")

    def start_listening(self):
        """Bắt đầu lắng nghe"""
        if not self.is_listening:
            self.is_listening = True
            self.listening_started.emit()
            self.status_changed.emit("Đang lắng nghe...")
            self.thread = ListeningThread(self)
            self.thread.start()

    def stop_listening(self):
        """Dừng lắng nghe"""
        if self.is_listening:
            self.is_listening = False
            self.listening_stopped.emit()
            self.status_changed.emit("Đã dừng")
            if self.thread:
                self.thread.wait(2000)

    def cleanup(self):
        """Dọn dẹp tài nguyên"""
        self.stop_listening()

    def is_alt_pressed(self):
        """Kiểm tra phím Alt có đang được nhấn"""
        return keyboard.is_pressed('alt')


class ListeningThread(QThread):
    """Thread xử lý việc lắng nghe và nhận dạng giọng nói sử dụng PyAudio"""
    
    def __init__(self, recognizer: SpeechRecognizer):
        super().__init__()
        self.recognizer = recognizer
        self.audio_queue = Queue()
        self.processing_thread = None

    def run(self):
        """Main thread loop - sử dụng sr.Microphone (PyAudio)"""
        # Start processing thread
        self.processing_thread = threading.Thread(
            target=self.process_audio_queue, 
            daemon=True
        )
        self.processing_thread.start()

        try:
            # Sử dụng sr.Microphone với PyAudio
            with sr.Microphone(sample_rate=16000) as source:
                # Calibrate cho ambient noise
                self.recognizer.status_changed.emit("Đang hiệu chỉnh micro...")
                self.recognizer.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                self.recognizer.status_changed.emit("Đang lắng nghe...")

                while self.recognizer.is_listening:
                    try:
                        # Listen với timeout
                        audio = self.recognizer.recognizer.listen(
                            source,
                            timeout=5,
                            phrase_time_limit=15
                        )

                        # Tính audio level
                        try:
                            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                            level = np.abs(audio_data).mean() / 32768.0
                            self.recognizer.audio_level.emit(min(level * 3, 1.0))
                        except Exception:
                            pass

                        # Đưa vào queue để xử lý
                        self.audio_queue.put(audio)

                    except sr.WaitTimeoutError:
                        self.recognizer.audio_level.emit(0.0)
                        continue
                    except Exception as e:
                        self.recognizer.error_occurred.emit(f"Lỗi thu âm: {str(e)}")

        except Exception as e:
            self.recognizer.error_occurred.emit(f"Lỗi microphone: {str(e)}")

    def process_audio_queue(self):
        """Xử lý queue audio trong background thread"""
        while self.recognizer.is_listening or not self.audio_queue.empty():
            try:
                audio = self.audio_queue.get(timeout=1)
                self.process_audio(audio)
                self.audio_queue.task_done()
            except Exception:
                continue

    def process_audio(self, audio):
        """Xử lý audio và nhận dạng giọng nói"""
        self.recognizer.status_changed.emit("Đang xử lý...")

        try:
            # Nhận dạng với Google Speech API
            text = self.recognizer.recognizer.recognize_google(
                audio, 
                language=self.recognizer.language
            )

            if text and text.strip():
                print(f"[Nhận dạng] {text}")
                self.recognizer.text_recognized.emit(text.strip())
                self.recognizer.status_changed.emit("Đang lắng nghe...")
            else:
                self.recognizer.status_changed.emit("Đang lắng nghe...")

        except sr.UnknownValueError:
            # Không nhận dạng được - bình thường
            self.recognizer.status_changed.emit("Đang lắng nghe...")
        except sr.RequestError as e:
            self.recognizer.error_occurred.emit(f"Lỗi API: {str(e)}")
        except Exception as e:
            self.recognizer.error_occurred.emit(f"Lỗi: {str(e)}")
