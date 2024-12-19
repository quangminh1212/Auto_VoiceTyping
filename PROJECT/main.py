import sys
import io
import os
import warnings
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow
from auth.google_auth import GoogleAuth
from browser.docs_controller import DocsController
from text.manager import TextManager
from system.interaction import SystemInteraction
from state.store import StateStore
from utils.logger import setup_logger
from config.config import Config

# Tắt các cảnh báo không cần thiết
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Tắt TensorFlow warnings
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'

def initialize_components():
    Config.setup_directories()
    logger = setup_logger()
    auth = GoogleAuth()
    docs_controller = DocsController()
    text_manager = TextManager()
    system_interaction = SystemInteraction()
    state_store = StateStore()
    
    return logger, auth, docs_controller, text_manager, system_interaction, state_store

def main():
    # Thiết lập DPI
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Thiết lập môi trường
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    os.environ['QT_SCALE_FACTOR'] = '1'
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Sử dụng style Fusion cho giao diện nhất quán
    
    components = initialize_components()
    if components:
        logger, auth, docs_controller, text_manager, system_interaction, state_store = components
        logger.info("Starting VoiceTyping application")
        
        main_window = MainWindow(auth, docs_controller, text_manager, system_interaction, state_store)
        main_window.show()
        
        sys.exit(app.exec())

if __name__ == "__main__":
    main()