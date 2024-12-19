from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time
import psutil
import os
from pathlib import Path

class DocsController:
    def __init__(self):
        self.logger = logging.getLogger('voicetyping')
        self.driver = None
        self.setup_chrome_options()
        self.initialize_browser()
        
    def setup_chrome_options(self):
        self.chrome_options = Options()
        
        # Tối ưu Chrome Options
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "download.default_directory": str(Path.home() / "Downloads"),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
        
        # Cấu hình cơ bản
        options = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-notifications",
            "--disable-infobars",
            "--disable-web-security",
            "--disable-features=IsolateOrigins,site-per-process",
            "--disable-site-isolation-trials",
            "--window-size=1280,720",
            "--remote-debugging-port=9222",
            f"--user-data-dir={str(Path.home() / '.chrome-automation')}",
            "--start-maximized"
        ]
        
        for option in options:
            self.chrome_options.add_argument(option)
            
        self.chrome_options.add_experimental_option("prefs", prefs)
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        self.chrome_options.add_experimental_option("useAutomationExtension", False)

    def kill_chrome_processes(self):
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if 'chrome' in proc.info['name'].lower():
                    try:
                        os.kill(proc.info['pid'], 9)
                    except:
                        pass
            time.sleep(1)  # Đợi processes đóng
        except:
            pass

    def initialize_browser(self):
        try:
            # Cleanup trước khi khởi tạo
            if self.driver:
                self.driver.quit()
            self.kill_chrome_processes()
            
            # Khởi tạo ChromeDriver với retry
            for attempt in range(3):
                try:
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
                    self.driver.set_page_load_timeout(30)
                    self.driver.implicitly_wait(10)
                    
                    # Mở Google Docs
                    self.driver.get("https://docs.google.com/document/u/0/create")
                    time.sleep(2)  # Đợi load
                    
                    self.logger.info("Browser initialized successfully")
                    return True
                except Exception as e:
                    self.logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                    if self.driver:
                        self.driver.quit()
                    time.sleep(2)  # Đợi trước khi retry
            
            raise Exception("Failed to initialize browser after 3 attempts")
            
        except Exception as e:
            self.logger.error(f"Browser initialization failed: {str(e)}")
            if self.driver:
                self.driver.quit()
            return False

    def start_voice_typing(self):
        try:
            if not self.driver:
                if not self.initialize_browser():
                    return False
                    
            # Sử dụng JavaScript để click
            script = """
                function clickVoiceButton() {
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        if (btn.getAttribute('aria-label') === 'Nhập bằng giọng nói') {
                            btn.click();
                            return true;
                        }
                    }
                    return false;
                }
                return clickVoiceButton();
            """
            result = self.driver.execute_script(script)
            if result:
                self.logger.info("Voice typing started")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to start voice typing: {str(e)}")
            return False

    def stop_voice_typing(self):
        try:
            if not self.driver:
                return False
                
            script = """
                function clickStopButton() {
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        if (btn.getAttribute('aria-label') === 'Dừng nhập bằng giọng nói') {
                            btn.click();
                            return true;
                        }
                    }
                    return false;
                }
                return clickStopButton();
            """
            result = self.driver.execute_script(script)
            if result:
                self.logger.info("Voice typing stopped")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to stop voice typing: {str(e)}")
            return False

    def get_text(self):
        try:
            if not self.driver:
                return ""
                
            script = """
                return document.querySelector('.kix-paragraphrenderer')?.innerText || '';
            """
            return self.driver.execute_script(script) or ""
            
        except Exception as e:
            self.logger.error(f"Failed to get text: {str(e)}")
            return ""

    def close(self):
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
            self.kill_chrome_processes()
            self.logger.info("Browser closed successfully")
        except Exception as e:
            self.logger.error(f"Failed to close browser: {str(e)}")

    def __del__(self):
        self.close()