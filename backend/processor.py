import nltk
from PyQt5.QtCore import QThread, pyqtSignal

class TextProcessor(QThread):
    text_processed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        nltk.download('punkt', quiet=True)

    def process_text(self, text):
        sentences = nltk.sent_tokenize(text)
        processed_sentences = [sentence.capitalize() for sentence in sentences]
        return ' '.join(processed_sentences)

    def run(self):
        processed_text = self.process_text(self.input_text)
        self.text_processed.emit(processed_text)

    def process_async(self, text):
        self.input_text = text
        self.start()
