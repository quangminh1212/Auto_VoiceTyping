import sys
from PyQt5.QtWidgets import QApplication
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

    def run(self):
        self.main_window.start_button.clicked.connect(self.start_voice_typing)
        self.main_window.stop_button.clicked.connect(self.stop_voice_typing)
        self.main_window.show()
        sys.exit(self.app.exec_())

    def start_voice_typing(self):
        self.main_window.status_label.setText("Trạng thái: Đang nhận diện...")
        self.main_window.start_button.setEnabled(False)
        self.main_window.stop_button.setEnabled(True)
        self.recognizer.start_listening()

    def stop_voice_typing(self):
        self.recognizer.stop_listening()
        self.main_window.status_label.setText("Trạng thái: Đã dừng")
        self.main_window.start_button.setEnabled(True)
        self.main_window.stop_button.setEnabled(False)

    def on_text_recognized(self, text):
        processed_text = self.processor.process_text(text)
        self.controller.type_text(processed_text)
        self.main_window.update_recognized_text(processed_text)
        self.main_window.status_label.setText("Trạng thái: Đã nhập văn bản")

if __name__ == "__main__":
    voice_typing_app = VoiceTypingApp()
    voice_typing_app.run()
