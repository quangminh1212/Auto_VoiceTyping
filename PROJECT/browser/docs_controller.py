from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time
from concurrent.futures import ThreadPoolExecutor
import atexit
import psutil
import os

class DocsController:
    def __init__(self):
        self.logger = logging.getLogger('voicetyping')
        self.driver = None
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.setup_chrome_options()
        self.initialize_browser()
        atexit.register(self.cleanup)
        
    def setup_chrome_options(self):
        self.chrome_options = Options()
        
        # Extreme Performance Optimizations
        prefs = {
            'profile.default_content_setting_values.notifications': 2,
            'profile.managed_default_content_settings.images': 2,
            'profile.managed_default_content_settings.javascript': 1,
            'profile.managed_default_content_settings.cookies': 1,
            'profile.managed_default_content_settings.plugins': 1,
            'profile.managed_default_content_settings.popups': 2,
            'profile.managed_default_content_settings.geolocation': 2,
            'profile.managed_default_content_settings.media_stream': 2,
            'disk-cache-size': 4096,
            'media.autoplay.enabled': False,
            'dom.ipc.plugins.enabled': False
        }
        
        # Core Options
        options = [
            '--headless=new',
            '--disable-gpu',
            '--disable-software-rasterizer',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-extensions',
            '--disable-logging',
            '--disable-notifications',
            '--disable-default-apps',
            '--disable-popup-blocking',
            '--disable-infobars',
            '--disable-translate',
            '--disable-features=TranslateUI',
            '--disable-web-security',
            '--disable-client-side-phishing-detection',
            '--disable-breakpad',
            '--disable-cast',
            '--disable-casting',
            '--disable-cloud-import',
            '--disable-component-update',
            '--disable-domain-reliability',
            '--disable-hang-monitor',
            '--disable-ipc-flooding-protection',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-background-timer-throttling',
            '--disable-background-networking',
            '--disable-prompt-on-repost',
            '--disable-sync',
            '--disable-zero-browsers-open-for-tests',
            '--no-default-browser-check',
            '--no-first-run',
            '--password-store=basic',
            '--use-mock-keychain',
            '--force-gpu-mem-available-mb=512',
            '--memory-model=low',
            '--disable-features=site-per-process',
            '--window-size=800,600',
            '--blink-settings=imagesEnabled=false'
        ]
        
        for option in options:
            self.chrome_options.add_argument(option)
            
        self.chrome_options.add_experimental_option('prefs', prefs)
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
    def kill_chrome_processes(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'chrome' in proc.info['name'].lower():
                    os.kill(proc.info['pid'], 9)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def initialize_browser(self):
        try:
            self.kill_chrome_processes()  # Cleanup existing processes
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
            self.driver.set_page_load_timeout(10)
            self.driver.implicitly_wait(5)
            
            # Preload Google Docs in background
            future = self.executor.submit(self.preload_docs)
            future.result(timeout=10)  # Wait max 10 seconds
            
        except Exception as e:
            self.logger.error(f"Browser initialization failed: {str(e)}")
            self.cleanup()
            raise

    def preload_docs(self):
        try:
            self.driver.get("https://docs.google.com/document/u/0/create")
            time.sleep(1)  # Minimal wait
            return True
        except Exception as e:
            self.logger.error(f"Preload failed: {str(e)}")
            return False

    def execute_js(self, script, timeout=5):
        try:
            return self.driver.execute_script(script)
        except Exception as e:
            self.logger.error(f"JS execution failed: {str(e)}")
            return None

    def start_voice_typing(self):
        script = """
        const btn = Array.from(document.querySelectorAll('button'))
            .find(b => b.getAttribute('aria-label') === 'Nhập bằng giọng nói');
        if(btn) { btn.click(); return true; }
        return false;
        """
        return self.execute_js(script)

    def stop_voice_typing(self):
        script = """
        const btn = Array.from(document.querySelectorAll('button'))
            .find(b => b.getAttribute('aria-label') === 'Dừng nhập bằng giọng nói');
        if(btn) { btn.click(); return true; }
        return false;
        """
        return self.execute_js(script)

    def get_text(self):
        script = "return document.querySelector('.kix-paragraphrenderer')?.innerText || '';"
        return self.execute_js(script) or ""

    def cleanup(self):
        try:
            if self.driver:
                self.driver.quit()
            self.executor.shutdown(wait=False)
            self.kill_chrome_processes()
        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")

    def __del__(self):
        self.cleanup()