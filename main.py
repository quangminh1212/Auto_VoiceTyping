import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from frontend.main_window import MainWindow
from backend.recognizer import SpeechRecognizer
from backend.processor import TextProcessor
from backend.controller import InputController

class VoiceTypingApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        self.recognizer = SpeechRecognizer()
        self.processor = TextProcessor()
        self.controller = InputController()

        self.recognizer.text_recognized.connect(self.on_text_recognized)
        
        self.text_buffer = ""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(100)  # Cập nhật mỗi 100ms

        self.app.aboutToQuit.connect(self.cleanup)

    def run(self):
        self.main_window.start_button.clicked.connect(self.start_voice_typing)
        self.main_window.stop_button.clicked.connect(self.stop_voice_typing)
        self.main_window.show()
        sys.exit(self.app.exec_())

    def start_voice_typing(self):
        self.main_window.start_recognition()
        self.recognizer.start_listening()

    def stop_voice_typing(self):
        self.recognizer.stop_listening()
        self.main_window.stop_recognition()

    def on_text_recognized(self, text):
        processed_text = self.processor.process_text(text)
        self.text_buffer += processed_text + " "

    def update_display(self):
        if self.text_buffer:
            self.main_window.update_recognized_text(self.text_buffer)
            self.controller.type_text(self.text_buffer)
            self.text_buffer = ""

    def cleanup(self):
        self.recognizer.cleanup()

if __name__ == "__main__":
    voice_typing_app = VoiceTypingApp()
    voice_typing_app.run()
