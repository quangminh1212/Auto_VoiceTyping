import speech_recognition as sr
import logging
import pyperclip
from PyQt6.QtWidgets import QMessageBox
import threading

class DocsController:
    def __init__(self):
        self.logger = logging.getLogger('voicetyping')
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_recording = False
        self.current_text = ""
        self.recording_thread = None

    def start_voice_typing(self):
        try:
            if self.is_recording:
                QMessageBox.warning(None, "Cảnh báo", "Đang trong quá trình ghi âm!")
                return False

            # Bắt đầu ghi âm trong thread riêng
            self.is_recording = True
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.start()
            
            self.logger.info("Voice recording started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start recording: {e}")
            return False

    def _record_audio(self):
        try:
            with self.microphone as source:
                # Điều chỉnh nhiễu môi trường
                self.recognizer.adjust_for_ambient_noise(source)
                
                while self.is_recording:
                    audio = self.recognizer.listen(source)
                    try:
                        text = self.recognizer.recognize_google(audio, language='vi-VN')
                        self.current_text += text + " "
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        self.logger.error(f"API Error: {e}")
                        break
                        
        except Exception as e:
            self.logger.error(f"Recording error: {e}")

    def stop_voice_typing(self):
        try:
            if not self.is_recording:
                QMessageBox.warning(None, "Cảnh báo", "Chưa bắt đầu ghi âm!")
                return False

            self.is_recording = False
            if self.recording_thread:
                self.recording_thread.join()
            
            self.logger.info("Voice recording stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop recording: {e}")
            return False

    def get_text(self):
        try:
            text = self.current_text
            pyperclip.copy(text)  # Copy to clipboard
            return text
            
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