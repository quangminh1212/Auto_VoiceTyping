import nltk
from PyQt5.QtCore import QObject, pyqtSignal

class TextProcessor(QObject):
    text_processed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        nltk.download('punkt', quiet=True)

    def process_text(self, text):
        # Tách câu
        sentences = nltk.sent_tokenize(text)
        
        # Xử lý từng câu
        processed_sentences = []
        for sentence in sentences:
            # Loại bỏ khoảng trắng thừa
            sentence = ' '.join(sentence.split())
            # Viết hoa chữ cái đầu câu
            sentence = sentence.capitalize()
            processed_sentences.append(sentence)
        
        # Kết hợp các câu đã xử lý
        processed_text = ' '.join(processed_sentences)
        return processed_text

    def process_async(self, text):
        processed_text = self.process_text(text)
        self.text_processed.emit(processed_text)
