import nltk
from PyQt5.QtCore import QObject, pyqtSignal

class TextProcessor(QObject):
    text_processed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        nltk.download('punkt', quiet=True)
        self.previous_text = ""

    def process_text(self, text):
        # Loại bỏ các từ trùng lặp
        words = text.split()
        unique_words = []
        for word in words:
            if not unique_words or word != unique_words[-1]:
                unique_words.append(word)
        processed_text = " ".join(unique_words)

        # Chỉ giữ lại phần văn bản mới
        if self.previous_text and processed_text.startswith(self.previous_text):
            processed_text = processed_text[len(self.previous_text):].strip()

        self.previous_text = text
        return processed_text

    def process_async(self, text):
        processed_text = self.process_text(text)
        self.text_processed.emit(processed_text)
