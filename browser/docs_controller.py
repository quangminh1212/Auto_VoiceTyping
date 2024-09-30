from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DocsController:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
    
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