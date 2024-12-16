"""
Voice Typing Application
Author: Bach Gia
Email: wuangming12@gmail.com
Version: 1.0.0
"""

import sys
from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow
from services.audio_service import AudioService
from controllers.docs_controller import DocsController
from utils.text_manager import TextManager
from utils.system_interaction import SystemInteraction
from utils.state_store import StateStore

def main():
    print("\n=== VOICE TYPING APP - DARK MODE ===")
    print("Author: Bach Gia")
    print("Email: wuangming12@gmail.com")
    print("Version: 1.0.0")
    
    app = QApplication(sys.argv)
    
    # Initialize components
    auth = None
    docs_controller = DocsController()
    text_manager = TextManager()
    system_interaction = SystemInteraction()
    state_store = StateStore()
    
    # Create and show window
    window = MainWindow(auth, docs_controller, text_manager, system_interaction, state_store)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 