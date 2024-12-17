"""
Voice Typing Application
Author: Bach Gia
Email: wuangming12@gmail.com
Version: 1.0.0
"""

import sys
import os
from PyQt6.QtWidgets import QApplication

# Thêm thư mục gốc vào PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from ui.main_window import MainWindow
    from services.audio_service import AudioService
    from controllers.docs_controller import DocsController
    from utils.text_manager import TextManager
    from utils.system_interaction import SystemInteraction
    from utils.state_store import StateStore
    
    print("Import thành công!")
except Exception as e:
    print(f"Lỗi import: {str(e)}")
    print(f"Python path: {sys.path}")
    sys.exit(1)

def main():
    print("\n=== VOICE TYPING APP - DARK MODE ===")
    print("Author: Bach Gia")
    print("Email: wuangming12@gmail.com")
    print("Version: 1.0.0")
    
    try:
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
        
    except Exception as e:
        print(f"Lỗi khởi động ứng dụng: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 