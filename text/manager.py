import pyperclip

class TextManager:
    def __init__(self):
        self.current_text = ""
    
    def set_text(self, text):
        self.current_text = text
        pyperclip.copy(text)
    
    def get_text(self):
        return self.current_text