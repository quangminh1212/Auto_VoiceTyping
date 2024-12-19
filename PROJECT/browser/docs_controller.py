from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

class DocsController:
    def __init__(self):
        self.logger = logging.getLogger('voicetyping')
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = None
        self.service = None
        self.initialize_browser()
    
    def initialize_browser(self):
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.open_docs()
            self.logger.info("Browser initialized successfully")
        except WebDriverException as e:
            self.logger.error(f"Failed to initialize browser: {str(e)}")
            raise Exception("Could not initialize Chrome browser. Please check if Chrome is installed.")
    
    def open_docs(self):
        try:
            self.driver.get("https://docs.google.com/document/create")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".docs-title-input"))
            )
            self.logger.info("Google Docs opened successfully")
        except Exception as e:
            self.logger.error(f"Failed to open Google Docs: {str(e)}")
            raise
    
    def start_voice_typing(self):
        try:
            if not self.driver:
                self.initialize_browser()
            
            voice_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Nhập bằng giọng nói']"))
            )
            voice_button.click()
            self.logger.info("Voice typing started")
        except Exception as e:
            self.logger.error(f"Failed to start voice typing: {str(e)}")
            raise
    
    def stop_voice_typing(self):
        try:
            if self.driver:
                voice_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Dừng nhập bằng giọng nói']"))
                )
                voice_button.click()
                self.logger.info("Voice typing stopped")
        except Exception as e:
            self.logger.error(f"Failed to stop voice typing: {str(e)}")
    
    def get_text(self):
        try:
            if self.driver:
                content = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".kix-paragraphrenderer"))
                )
                return content.text
        except Exception as e:
            self.logger.error(f"Failed to get text: {str(e)}")
            return ""
    
    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.logger.info("Browser closed")
    
    def __del__(self):
        self.close()
    
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