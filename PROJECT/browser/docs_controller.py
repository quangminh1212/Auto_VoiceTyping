import logging
import pyperclip
import time
from PyQt6.QtWidgets import QMessageBox

class DocsController:
    def __init__(self):
        self.logger = logging.getLogger('voicetyping')
        self.is_recording = False
        self.last_text = ""
        self.instructions = {
            'prepare': 'Vui lòng mở Google Docs và chọn Tools > Voice Typing',
            'start': '1. Click vào nút microphone để bắt đầu ghi âm',
            'stop': '2. Click lại vào microphone để dừng ghi âm',
            'copy': '3. Ctrl + A và Ctrl + C để copy text',
        }
        self.show_instructions()

    def show_instructions(self):
        try:
            message = "\n".join([
                "HƯỚNG DẪN SỬ DỤNG:",
                "----------------",
                self.instructions['prepare'],
                self.instructions['start'],
                self.instructions['stop'],
                self.instructions['copy'],
                "\nLưu ý: Cần mở Google Docs trước khi bắt đầu!"
            ])
            QMessageBox.information(None, "Hướng dẫn", message)
            self.logger.info("Instructions shown")
            return True
        except Exception as e:
            self.logger.error(f"Failed to show instructions: {e}")
            return False

    def start_voice_typing(self):
        try:
            if self.is_recording:
                QMessageBox.warning(None, "Cảnh báo", "Đang trong quá trình ghi âm!")
                return False
                
            message = "\n".join([
                "BẮT ĐẦU GHI ÂM:",
                "1. Click vào biểu tượng microphone",
                "2. Nói to và rõ ràng",
                "3. Đợi văn bản xuất hiện"
            ])
            QMessageBox.information(None, "Bắt đầu ghi âm", message)
            
            self.is_recording = True
            self.logger.info("Voice typing started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start recording: {e}")
            return False

    def stop_voice_typing(self):
        try:
            if not self.is_recording:
                QMessageBox.warning(None, "Cảnh báo", "Chưa bắt đầu ghi âm!")
                return False
                
            message = "Click vào microphone để dừng ghi âm"
            QMessageBox.information(None, "Dừng ghi âm", message)
            
            self.is_recording = False
            self.logger.info("Voice typing stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop recording: {e}")
            return False

    def get_text(self):
        try:
            message = "\n".join([
                "LẤY VĂN BẢN:",
                "1. Nhấn Ctrl + A để chọn toàn bộ",
                "2. Nhấn Ctrl + C để copy",
                "3. Click OK để tiếp tục"
            ])
            QMessageBox.information(None, "Lấy văn bản", message)
            
            # Đợi người dùng copy
            time.sleep(1)
            current_text = pyperclip.paste()
            
            if current_text == self.last_text:
                QMessageBox.warning(None, "Cảnh báo", "Chưa copy văn bản mới!")
                return ""
                
            self.last_text = current_text
            if current_text:
                QMessageBox.information(None, "Thành công", "Đã lấy văn bản thành công!")
            
            return current_text
            
        except Exception as e:
            self.logger.error(f"Failed to get text: {e}")
            return ""

    def close(self):
        try:
            if self.is_recording:
                self.stop_voice_typing()
            message = "Cảm ơn bạn đã sử dụng!"
            QMessageBox.information(None, "Kết thúc", message)
            self.logger.info("Application closed")
        except Exception as e:
            self.logger.error(f"Failed to close: {e}")