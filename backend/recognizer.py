"""
Voice Recognition Engine - Hỗ trợ nhận dạng giọng nói với Google Speech API
Sử dụng sounddevice thay vì PyAudio để tương thích với Python 3.14+
"""

import os
import sys
import io
import wave
import warnings
import time
import threading
import tempfile
from queue import Queue
from enum import Enum

import numpy as np
import sounddevice as sd
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


class SoundDeviceMicrophone:
    """
    Custom microphone class sử dụng sounddevice thay vì PyAudio
    Tương thích với speech_recognition
    """
    
    def __init__(self, sample_rate=16000, chunk_size=1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.stream = None
        self.audio_buffer = []
        self.is_recording = False
        self.SAMPLE_WIDTH = 2  # 16-bit audio
        self.SAMPLE_RATE = sample_rate
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        
    def start(self):
        """Bắt đầu thu âm"""
        self.audio_buffer = []
        self.is_recording = True
        
    def stop(self):
        """Dừng thu âm"""
        self.is_recording = False
        
    def record(self, duration: float) -> sr.AudioData:
        """Thu âm trong khoảng thời gian nhất định"""
        frames = int(duration * self.sample_rate)
        recording = sd.rec(frames, samplerate=self.sample_rate, channels=1, dtype='int16')
        sd.wait()
        
        # Chuyển đổi sang bytes
        audio_bytes = recording.tobytes()
        return sr.AudioData(audio_bytes, self.sample_rate, self.SAMPLE_WIDTH)
    
    def listen_until_silence(self, timeout=5, phrase_time_limit=15, 
                              energy_threshold=300, pause_threshold=0.8) -> sr.AudioData:
        """
        Lắng nghe cho đến khi phát hiện im lặng
        Trả về AudioData tương thích với speech_recognition
        """
        frames = []
        silence_frames = 0
        silence_threshold = int(pause_threshold * self.sample_rate / self.chunk_size)
        max_frames = int(phrase_time_limit * self.sample_rate / self.chunk_size)
        timeout_frames = int(timeout * self.sample_rate / self.chunk_size)
        
        speech_started = False
        frame_count = 0
        
        def audio_callback(indata, frames_count, time_info, status):
            nonlocal frames, silence_frames, speech_started, frame_count
            
            if not self.is_recording:
                return
                
            # Tính energy của frame
            energy = np.abs(indata).mean() * 32768
            
            if energy > energy_threshold:
                speech_started = True
                silence_frames = 0
                frames.append(indata.copy())
            elif speech_started:
                silence_frames += 1
                frames.append(indata.copy())
            
            frame_count += 1
        
        self.is_recording = True
        
        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=1, 
                               dtype='int16', blocksize=self.chunk_size,
                               callback=audio_callback):
                start_time = time.time()
                
                while self.is_recording:
                    time.sleep(0.05)
                    
                    # Check timeout
                    elapsed = time.time() - start_time
                    if not speech_started and elapsed > timeout:
                        raise TimeoutError("Hết thời gian chờ giọng nói")
                    
                    # Check phrase time limit
                    if speech_started and elapsed > phrase_time_limit:
                        break
                    
                    # Check silence after speech
                    if speech_started and silence_frames >= silence_threshold:
                        break
                    
                    # Max frames check
                    if frame_count >= max_frames:
                        break
        except Exception as e:
            if "Hết thời gian" in str(e):
                raise sr.WaitTimeoutError(str(e))
            raise
        
        if not frames:
            raise sr.WaitTimeoutError("Không có dữ liệu âm thanh")
        
        # Combine all frames
        audio_data = np.concatenate(frames)
        audio_bytes = audio_data.tobytes()
        
        return sr.AudioData(audio_bytes, self.sample_rate, self.SAMPLE_WIDTH)
    
    def get_audio_level(self, duration=0.1) -> float:
        """Lấy mức âm thanh hiện tại"""
        try:
            frames = int(duration * self.sample_rate)
            recording = sd.rec(frames, samplerate=self.sample_rate, channels=1, dtype='int16')
            sd.wait()
            level = np.abs(recording).mean() / 32768.0
            return min(level * 3, 1.0)
        except Exception:
            return 0.0


class SpeechRecognizer(QObject):
    """
    Speech Recognizer với hỗ trợ nhiều engine
    Sử dụng Google Speech API mặc định
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
        self.recognizer.pause_threshold = 0.5
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.3

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
    """Thread xử lý việc lắng nghe và nhận dạng giọng nói"""
    
    def __init__(self, recognizer: SpeechRecognizer):
        super().__init__()
        self.recognizer = recognizer
        self.audio_queue = Queue()
        self.processing_thread = None
        self.microphone = SoundDeviceMicrophone(sample_rate=16000)

    def run(self):
        """Main thread loop"""
        # Start processing thread
        self.processing_thread = threading.Thread(
            target=self.process_audio_queue, 
            daemon=True
        )
        self.processing_thread.start()

        try:
            self.recognizer.status_changed.emit("Đang khởi tạo micro...")
            
            with self.microphone:
                self.recognizer.status_changed.emit("Đang lắng nghe...")
                
                while self.recognizer.is_listening:
                    try:
                        # Listen với timeout
                        self.microphone.start()
                        audio = self.microphone.listen_until_silence(
                            timeout=3,
                            phrase_time_limit=15,
                            energy_threshold=self.recognizer.recognizer.energy_threshold,
                            pause_threshold=self.recognizer.recognizer.pause_threshold
                        )
                        self.microphone.stop()

                        # Emit audio level
                        try:
                            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                            level = np.abs(audio_data).mean() / 32768.0
                            self.recognizer.audio_level.emit(min(level * 3, 1.0))
                        except Exception:
                            pass

                        self.audio_queue.put(audio)

                    except sr.WaitTimeoutError:
                        self.recognizer.audio_level.emit(0.0)
                        continue
                    except TimeoutError:
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
            text = self._recognize_google(audio)

            if text and text.strip():
                self.recognizer.text_recognized.emit(text.strip())
                self.recognizer.status_changed.emit("Đang lắng nghe...")
            else:
                self.recognizer.status_changed.emit("Đang lắng nghe...")

        except sr.UnknownValueError:
            self.recognizer.status_changed.emit("Đang lắng nghe...")
        except sr.RequestError as e:
            self.recognizer.error_occurred.emit(f"Lỗi API: {str(e)}")
        except Exception as e:
            self.recognizer.error_occurred.emit(f"Lỗi: {str(e)}")

    def _recognize_google(self, audio) -> str:
        """Nhận dạng với Google Speech API"""
        lang = self.recognizer.language
        return self.recognizer.recognizer.recognize_google(audio, language=lang)
