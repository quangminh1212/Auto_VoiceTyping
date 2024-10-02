import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from PyQt6.QtWidgets import QApplication

from auth.google_auth import GoogleAuth
from browser.docs_controller import DocsController
from state.store import StateStore
from system.interaction import SystemInteraction
from text.manager import TextManager
from ui.main_window import MainWindow
from utils.logger import setup_logger

def main():
    logger = setup_logger()
    logger.info("Khởi động ứng dụng VoiceTyping")

    app = QApplication(sys.argv)

    auth = GoogleAuth()
    docs_controller = DocsController()
    text_manager = TextManager()
    system_interaction = SystemInteraction()
    state_store = StateStore()

    main_window = MainWindow(auth, docs_controller, text_manager, system_interaction, state_store)
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()