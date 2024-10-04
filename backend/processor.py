import nltk
nltk.download('punkt')

class TextProcessor:
    def __init__(self):
        pass

    def process_text(self, text):
        # Tách câu
        sentences = nltk.sent_tokenize(text)
        
        # Xử lý từng câu
        processed_sentences = []
        for sentence in sentences:
            # Viết hoa chữ cái đầu câu
            processed_sentence = sentence.capitalize()
            processed_sentences.append(processed_sentence)
        
        # Kết hợp các câu đã xử lý
        processed_text = ' '.join(processed_sentences)
        return processed_text
