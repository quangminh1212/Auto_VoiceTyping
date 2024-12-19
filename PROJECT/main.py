import sys
import io
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
from utils.error_handler import handle_errors

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

@handle_errors
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
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    
    components = initialize_components()
    if components:
        logger, auth, docs_controller, text_manager, system_interaction, state_store = components
        logger.info("Starting VoiceTyping application")
        
        main_window = MainWindow(auth, docs_controller, text_manager, system_interaction, state_store)
        main_window.show()
        
        sys.exit(app.exec())

if __name__ == "__main__":
    main()