import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from auth.google_auth import GoogleAuth
from browser.docs_controller import DocsController
from text.manager import TextManager
from system.interaction import SystemInteraction
from state.store import StateStore
from utils.logger import setup_logger

def generate_project_structure():
    project_structure = "# Cấu trúc dự án VoiceTyping\n\n"
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py') and file != 'main.py':
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path)
                project_structure += f"## {relative_path}\n```python\n"
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    project_structure += f.read()
                
                project_structure += "\n```\n\n"
    
    with open('project_structure.md', 'w', encoding='utf-8') as f:
        f.write(project_structure)

def main():
    # Cập nhật project_structure.md
    generate_project_structure()

    # Thiết lập logger
    logger = setup_logger()

    # Khởi tạo ứng dụng PyQt
    app = QApplication(sys.argv)

    # Khởi tạo các thành phần
    auth = GoogleAuth()
    docs_controller = DocsController()
    text_manager = TextManager()
    system_interaction = SystemInteraction()
    state_store = StateStore()

    # Khởi tạo cửa sổ chính
    main_window = MainWindow(auth, docs_controller, text_manager, system_interaction, state_store)
    main_window.show()

    # Chạy ứng dụng
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
