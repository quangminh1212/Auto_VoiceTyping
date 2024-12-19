import pyautogui
import keyboard
import time
import logging
import webbrowser
import psutil
import os
from pathlib import Path

class DocsController:
    def __init__(self):
        self.logger = logging.getLogger('voicetyping')
        self.is_recording = False
        self.setup_shortcuts()
        pyautogui.FAILSAFE = True
        
    def setup_shortcuts(self):
        # Phím tắt cho Google Docs
        self.shortcuts = {
            'voice_typing': 'ctrl+shift+s',  # Phím tắt mở voice typing
            'stop_voice': 'esc',             # Phím tắt dừng voice typing
            'copy': 'ctrl+a, ctrl+c',        # Copy toàn bộ văn bản
        }
        
    def open_google_docs(self):
        try:
            # Mở Google Docs trong trình duyệt mặc định
            webbrowser.open('https://docs.google.com/document/u/0/create', new=2)
            time.sleep(3)  # Đợi trang load
            
            # Maximize cửa sổ
            pyautogui.hotkey('win', 'up')
            time.sleep(1)
            
            self.logger.info("Google Docs opened successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open Google Docs: {str(e)}")
            return False

    def start_voice_typing(self):
        try:
            if not self.is_recording:
                # Mở voice typing bằng phím tắt
                keyboard.send(self.shortcuts['voice_typing'])
                time.sleep(1)
                
                # Xác nhận voice typing đã bật
                self.is_recording = True
                self.logger.info("Voice typing started")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to start voice typing: {str(e)}")
            return False

    def stop_voice_typing(self):
        try:
            if self.is_recording:
                # Dừng voice typing
                keyboard.send(self.shortcuts['stop_voice'])
                time.sleep(0.5)
                
                self.is_recording = False
                self.logger.info("Voice typing stopped")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to stop voice typing: {str(e)}")
            return False

    def get_text(self):
        try:
            # Copy toàn bộ văn bản
            for shortcut in self.shortcuts['copy'].split(', '):
                keyboard.send(shortcut)
                time.sleep(0.2)
            
            # Lấy text từ clipboard
            import pyperclip
            text = pyperclip.paste()
            return text
            
        except Exception as e:
            self.logger.error(f"Failed to get text: {str(e)}")
            return ""

    def close(self):
        try:
            # Đóng tab hiện tại
            keyboard.send('ctrl+w')
            self.logger.info("Browser tab closed successfully")
        except Exception as e:
            self.logger.error(f"Failed to close browser: {str(e)}")

    def __del__(self):
        self.close()