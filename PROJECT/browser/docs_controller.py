import logging
import pyperclip

class DocsController:
    def __init__(self):
        self.logger = logging.getLogger('voicetyping')
        self.is_recording = False
        self.instructions = {
            'start': 'Nhấn Ctrl + Shift + S để bắt đầu ghi âm',
            'stop': 'Nhấn ESC để dừng ghi âm',
            'copy': 'Nhấn Ctrl + A rồi Ctrl + C để copy text',
            'close': 'Nhấn Ctrl + W để đóng tab'
        }
        self.show_instructions()

    def show_instructions(self):
        try:
            print("\nHướng dẫn sử dụng:")
            for action, guide in self.instructions.items():
                print(f"- {guide}")
            self.logger.info("Instructions shown")
            return True
        except Exception as e:
            self.logger.error(f"Failed to show instructions: {e}")
            return False

    def start_voice_typing(self):
        print(f"\n{self.instructions['start']}")
        self.is_recording = True
        return True

    def stop_voice_typing(self):
        print(f"\n{self.instructions['stop']}")
        self.is_recording = False
        return True

    def get_text(self):
        print(f"\n{self.instructions['copy']}")
        return pyperclip.paste()

    def close(self):
        print(f"\n{self.instructions['close']}")
        self.logger.info("Instructions shown for closing")