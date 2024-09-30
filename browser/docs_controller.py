from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class DocsController:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.service = None
    
    def open_docs(self):
        self.driver.get("https://docs.google.com/document/create")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".docs-title-input"))
        )
    
    def start_voice_typing(self):
        voice_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Nhập bằng giọng nói']")
        voice_button.click()
    
    def stop_voice_typing(self):
        voice_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Dừng nhập bằng giọng nói']")
        voice_button.click()
    
    def get_text(self):
        content = self.driver.find_element(By.CSS_SELECTOR, ".kix-paragraphrenderer")
        return content.text
    
    def close(self):
        self.driver.quit()
    
    def initialize_service(self, credentials):
        try:
            self.service = build('docs', 'v1', credentials=credentials)
        except NameError:
            print("Không thể khởi tạo service do thiếu thư viện Google Client.")

    def insert_text(self, document_id, text):
        if not self.service:
            print("Service chưa được khởi tạo.")
            return False

        try:
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1,
                        },
                        'text': text
                    }
                }
            ]
            self.service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
            return True
        except Exception as error:
            print(f'Đã xảy ra lỗi: {error}')
            return False

    def get_document_content(self, document_id):
        if not self.service:
            print("Service chưa được khởi tạo.")
            return None

        try:
            document = self.service.documents().get(documentId=document_id).execute()
            return document.get('body').get('content')
        except Exception as error:
            print(f'Đã xảy ra lỗi: {error}')
            return None