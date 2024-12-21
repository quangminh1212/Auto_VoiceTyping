import logging
import pyperclip
from PyQt6.QtWidgets import QMessageBox
import threading
import time

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_ENABLED = True
except ImportError:
    SPEECH_RECOGNITION_ENABLED = False

class DocsController:
    def __init__(self):
        self.logger = logging.getLogger('voicetyping')
        self.is_recording = False
        self.current_text = ""
        self.recording_thread = None
        
        # Kiểm tra và khởi tạo speech recognition
        if SPEECH_RECOGNITION_ENABLED:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                # Test microphone
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.logger.info("Speech recognition initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize speech recognition: {e}")
                QMessageBox.critical(None, "Lỗi", 
                    "Không thể khởi tạo microphone.\nVui lòng kiểm tra thiết bị âm thanh.")
                SPEECH_RECOGNITION_ENABLED = False
        else:
            QMessageBox.warning(None, "Cảnh báo", 
                "Chức năng nhận diện giọng nói không khả dụng.\nVui lòng cài đặt lại các thư viện cần thiết.")

    def start_voice_typing(self):
        if not SPEECH_RECOGNITION_ENABLED:
            QMessageBox.warning(None, "Cảnh báo", 
                "Chức năng nhận diện giọng nói không khả dụng!")
            return False
            
        try:
            if self.is_recording:
                QMessageBox.warning(None, "Cảnh báo", "Đang trong quá trình ghi âm!")
                return False

            # Kiểm tra microphone
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

            # Bắt đầu ghi âm trong thread riêng
            self.is_recording = True
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.daemon = True  # Thread sẽ tự đóng khi chương trình kết thúc
            self.recording_thread.start()
            
            QMessageBox.information(None, "Thông báo", "Bắt đầu ghi âm.\nHãy nói to và rõ ràng!")
            self.logger.info("Voice recording started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start recording: {e}")
            QMessageBox.critical(None, "Lỗi", f"Không thể bắt đầu ghi âm: {str(e)}")
            return False

    def _record_audio(self):
        try:
            with self.microphone as source:
                while self.is_recording:
                    try:
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        text = self.recognizer.recognize_google(audio, language='vi-VN')
                        self.current_text += text + " "
                        self.logger.info(f"Recognized: {text}")
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        self.logger.error(f"API Error: {e}")
                        QMessageBox.warning(None, "Cảnh báo", 
                            "Lỗi kết nối API Google Speech Recognition")
                        break
                    time.sleep(0.1)  # Tránh CPU cao
                        
        except Exception as e:
            self.logger.error(f"Recording error: {e}")
            QMessageBox.critical(None, "Lỗi", f"Lỗi ghi âm: {str(e)}")

    def stop_voice_typing(self):
        try:
            if not self.is_recording:
                QMessageBox.warning(None, "Cảnh báo", "Chưa bắt đầu ghi âm!")
                return False

            self.is_recording = False
            if self.recording_thread and self.recording_thread.is_alive():
                self.recording_thread.join(timeout=2)
            
            QMessageBox.information(None, "Thông báo", "Đã dừng ghi âm!")
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
                QMessageBox.information(None, "Thành công", 
                    "Đã copy văn bản vào clipboard!")
            return text
            
        except Exception as e:
            self.logger.error(f"Failed to get text: {e}")
            QMessageBox.critical(None, "Lỗi", f"Không thể lấy văn bản: {str(e)}")
            return ""

    def close(self):
        try:
            if self.is_recording:
                self.stop_voice_typing()
            self.logger.info("Application closed")
        except Exception as e:
            self.logger.error(f"Failed to close: {e}")