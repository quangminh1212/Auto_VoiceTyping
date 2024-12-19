from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from googleapiclient.discovery import build
import logging
import os

class DocsController:
    def __init__(self):
        self.logger = logging.getLogger('voicetyping')
        self.setup_chrome_options()
        self.driver = None
        self.service = None
        
    def setup_chrome_options(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless=new")  # Sử dụng headless mới
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--remote-debugging-port=9222")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument("--disable-infobars")
        
        # Thêm user agent
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    def initialize_browser(self):
        try:
            if self.driver:
                return

            # Sử dụng webdriver_manager để tự động tải ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
            
            # Thiết lập timeout mặc định
            self.driver.implicitly_wait(10)
            self.driver.set_script_timeout(30)
            self.driver.set_page_load_timeout(30)
            
            self.open_docs()
            self.logger.info("Browser initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize browser: {str(e)}")
            if self.driver:
                self.driver.quit()
                self.driver = None
            raise Exception(f"Could not initialize Chrome browser: {str(e)}")
    
    def open_docs(self):
        try:
            self.driver.get("https://docs.google.com")
            # Đợi cho trang load xong
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            self.logger.info("Google Docs opened successfully")
        except Exception as e:
            self.logger.error(f"Failed to open Google Docs: {str(e)}")
            raise
    
    def start_voice_typing(self):
        try:
            if not self.driver:
                self.initialize_browser()
            
            # Tìm và click nút voice typing
            voice_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Nhập bằng giọng nói"]'))
            )
            self.driver.execute_script("arguments[0].click();", voice_button)
            self.logger.info("Voice typing started")
            
        except Exception as e:
            self.logger.error(f"Failed to start voice typing: {str(e)}")
            self.initialize_browser()  # Thử khởi tạo lại nếu có lỗi
    
    def stop_voice_typing(self):
        try:
            if not self.driver:
                return
                
            voice_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Dừng nhập bằng giọng nói"]'))
            )
            self.driver.execute_script("arguments[0].click();", voice_button)
            self.logger.info("Voice typing stopped")
            
        except Exception as e:
            self.logger.error(f"Failed to stop voice typing: {str(e)}")
    
    def get_text(self):
        try:
            if not self.driver:
                return ""
                
            content = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".kix-paragraphrenderer"))
            )
            return content.text
            
        except Exception as e:
            self.logger.error(f"Failed to get text: {str(e)}")
            return ""
    
    def close(self):
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.logger.info("Browser closed successfully")
        except Exception as e:
            self.logger.error(f"Failed to close browser: {str(e)}")
    
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