from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time
from threading import Lock

class DocsController:
    def __init__(self):
        self.logger = logging.getLogger('voicetyping')
        self.driver = None
        self.lock = Lock()
        self.is_initialized = False
        self.setup_chrome_options()
        
    def setup_chrome_options(self):
        self.chrome_options = Options()
        
        # Performance optimizations
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-software-rasterizer')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--disable-logging')
        self.chrome_options.add_argument('--disable-notifications')
        self.chrome_options.add_argument('--disable-default-apps')
        self.chrome_options.add_argument('--disable-popup-blocking')
        
        # Memory optimizations
        self.chrome_options.add_argument('--js-flags=--expose-gc')
        self.chrome_options.add_argument('--single-process')
        self.chrome_options.add_argument('--disable-application-cache')
        self.chrome_options.add_argument('--aggressive-cache-discard')
        self.chrome_options.add_argument('--disable-offline-load-stale-cache')
        
        # Network optimizations
        self.chrome_options.add_argument('--dns-prefetch-disable')
        self.chrome_options.add_argument('--no-proxy-server')
        
        # Headless mode optimizations
        self.chrome_options.add_argument('--headless=new')
        self.chrome_options.add_argument('--window-size=1920,1080')
        
        # Additional performance settings
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome_options.add_experimental_option('prefs', {
            'profile.default_content_setting_values.notifications': 2,
            'profile.managed_default_content_settings.images': 2,
            'profile.managed_default_content_settings.javascript': 1
        })

    def initialize_browser(self, force=False):
        with self.lock:
            if self.is_initialized and not force:
                return True
                
            try:
                if self.driver:
                    self.driver.quit()
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
                self.driver.set_page_load_timeout(30)
                self.driver.implicitly_wait(10)
                
                # Preload Google Docs
                self.driver.get("https://docs.google.com/document/u/0/create")
                time.sleep(2)  # Allow initial load
                
                # Wait for essential elements
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                self.is_initialized = True
                self.logger.info("Browser initialized successfully")
                return True
                
            except Exception as e:
                self.logger.error(f"Browser initialization failed: {str(e)}")
                self.is_initialized = False
                if self.driver:
                    self.driver.quit()
                    self.driver = None
                return False

    def execute_with_retry(self, action, max_retries=2):
        for attempt in range(max_retries):
            try:
                if not self.is_initialized:
                    if not self.initialize_browser():
                        raise Exception("Failed to initialize browser")
                return action()
            except Exception as e:
                self.logger.error(f"Action failed (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    self.initialize_browser(force=True)
                else:
                    raise

    def start_voice_typing(self):
        def _start():
            try:
                # Tìm và click nút voice typing bằng JavaScript
                script = """
                    var buttons = document.querySelectorAll('button');
                    for(var i=0; i<buttons.length; i++) {
                        if(buttons[i].getAttribute('aria-label') === 'Nhập bằng giọng nói') {
                            buttons[i].click();
                            return true;
                        }
                    }
                    return false;
                """
                result = self.driver.execute_script(script)
                if not result:
                    raise Exception("Voice typing button not found")
                return True
            except Exception as e:
                raise Exception(f"Failed to start voice typing: {str(e)}")

        return self.execute_with_retry(_start)

    def stop_voice_typing(self):
        def _stop():
            try:
                script = """
                    var buttons = document.querySelectorAll('button');
                    for(var i=0; i<buttons.length; i++) {
                        if(buttons[i].getAttribute('aria-label') === 'Dừng nhập bằng giọng nói') {
                            buttons[i].click();
                            return true;
                        }
                    }
                    return false;
                """
                result = self.driver.execute_script(script)
                if not result:
                    raise Exception("Stop button not found")
                return True
            except Exception as e:
                raise Exception(f"Failed to stop voice typing: {str(e)}")

        return self.execute_with_retry(_stop)

    def get_text(self):
        def _get_text():
            try:
                script = """
                    return document.querySelector('.kix-paragraphrenderer').innerText;
                """
                text = self.driver.execute_script(script)
                return text or ""
            except Exception as e:
                raise Exception(f"Failed to get text: {str(e)}")

        return self.execute_with_retry(_get_text)

    def close(self):
        with self.lock:
            try:
                if self.driver:
                    self.driver.quit()
                    self.driver = None
                self.is_initialized = False
                self.logger.info("Browser closed successfully")
            except Exception as e:
                self.logger.error(f"Failed to close browser: {str(e)}")

    def __del__(self):
        self.close()