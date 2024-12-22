import logging
import pyperclip
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal
import threading
import time
import speech_recognition as sr

class DocsController(QObject):
    text_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('voicetyping')
        self.is_recording = False
        self.current_text = ""
        self.recording_thread = None
        self.speech_enabled = False
        self.recognizer = None
        self.microphone = None
        
        # Khởi tạo speech recognition
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Test microphone
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.speech_enabled = True
            self.logger.info("Speech recognition initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Speech recognition init error: {e}")
            QMessageBox.warning(None, "Cảnh báo", 
                "Chức năng nhận diện giọng nói không khả dụng.\nVui lòng kiểm tra microphone và thư viện.")
            self.speech_enabled = False

    def _record_audio(self):
        if not self.speech_enabled or not self.recognizer or not self.microphone:
            return

        try:
            with self.microphone as source:
                while self.is_recording:
                    try:
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        text = self.recognizer.recognize_google(audio, language='vi-VN')
                        
                        # Thêm text mới và emit signal
                        self.current_text += text + " "
                        self.text_received.emit(text)
                        
                        self.logger.info(f"Recognized: {text}")
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        self.logger.error(f"API Error: {e}")
                        self.text_received.emit("[Lỗi kết nối API]")
                        break
                    except Exception as e:
                        self.logger.error(f"Recognition error: {e}")
                        continue
                    time.sleep(0.1)
                        
        except Exception as e:
            self.logger.error(f"Recording error: {e}")
            self.text_received.emit("[Lỗi ghi âm]")

    def start_voice_typing(self):
        if not self.speech_enabled:
            QMessageBox.warning(None, "Cảnh báo", 
                "Chức năng nhận diện giọng nói không khả dụng!")
            return False
            
        try:
            if self.is_recording:
                QMessageBox.warning(None, "Cảnh báo", "Đang trong quá trình ghi âm!")
                return False

            # Bắt đầu ghi âm trong thread riêng
            self.is_recording = True
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            
            self.logger.info("Voice recording started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start recording: {e}")
            QMessageBox.critical(None, "Lỗi", f"Không thể bắt đầu ghi âm: {str(e)}")
            return False

    def stop_voice_typing(self):
        try:
            if not self.is_recording:
                QMessageBox.warning(None, "Cảnh báo", "Chưa bắt đầu ghi âm!")
                return False

            self.is_recording = False
            if self.recording_thread and self.recording_thread.is_alive():
                self.recording_thread.join(timeout=2)
            
            self.logger.info("Voice recording stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop recording: {e}")
            QMessageBox.critical(None, "Lỗi", f"Không thể dừng ghi âm: {str(e)}")
            return False

    def get_text(self):
        try:
            text = self.current_text.strip()
            if text:
                pyperclip.copy(text)
                return text
            return ""
            
        except Exception as e:
            self.logger.error(f"Failed to get text: {e}")
            return ""

    def close(self):
        try:
            if self.is_recording:
                self.stop_voice_typing()
            self.logger.info("Application closed")
        except Exception as e:
            self.logger.error(f"Failed to close: {e}")