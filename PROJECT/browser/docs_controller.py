import webbrowser
import time
import logging
import pyperclip
from pynput.keyboard import Controller, Key

class DocsController:
    def __init__(self):
        self.logger = logging.getLogger('voicetyping')
        self.keyboard = Controller()
        self.is_recording = False
        self.docs_url = 'https://docs.google.com/document/u/0/create'
        self.open_docs()

    def open_docs(self):
        try:
            webbrowser.open(self.docs_url)
            time.sleep(2)  # Đợi docs mở
            self.logger.info("Google Docs opened")
            return True
        except Exception as e:
            self.logger.error(f"Failed to open docs: {e}")
            return False

    def press_keys(self, *keys):
        try:
            for key in keys:
                self.keyboard.press(key)
            for key in reversed(keys):
                self.keyboard.release(key)
            time.sleep(0.5)
        except Exception as e:
            self.logger.error(f"Key press failed: {e}")

    def start_voice_typing(self):
        try:
            if not self.is_recording:
                # Ctrl + Shift + S để bật voice typing
                self.press_keys(Key.ctrl, Key.shift, 's')
                self.is_recording = True
                self.logger.info("Voice typing started")
                return True
        except Exception as e:
            self.logger.error(f"Failed to start voice: {e}")
            return False

    def stop_voice_typing(self):
        try:
            if self.is_recording:
                # ESC để tắt voice typing
                self.press_keys(Key.esc)
                self.is_recording = False
                self.logger.info("Voice typing stopped")
                return True
        except Exception as e:
            self.logger.error(f"Failed to stop voice: {e}")
            return False

    def get_text(self):
        try:
            # Ctrl + A để chọn text
            self.press_keys(Key.ctrl, 'a')
            # Ctrl + C để copy
            self.press_keys(Key.ctrl, 'c')
            return pyperclip.paste()
        except Exception as e:
            self.logger.error(f"Failed to get text: {e}")
            return ""

    def close(self):
        try:
            # Ctrl + W để đóng tab
            self.press_keys(Key.ctrl, 'w')
            self.logger.info("Tab closed")
        except Exception as e:
            self.logger.error(f"Failed to close: {e}")