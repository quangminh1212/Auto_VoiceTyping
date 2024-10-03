import sys
import io
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from auth.google_auth import GoogleAuth
from browser.docs_controller import DocsController
from text.manager import TextManager
from system.interaction import SystemInteraction
from state.store import StateStore
from utils.logger import setup_logger

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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