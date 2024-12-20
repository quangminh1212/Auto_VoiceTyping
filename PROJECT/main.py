import sys
import logging
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from browser.docs_controller import DocsController
from utils.logger import setup_logger

def main():
    # Khởi tạo logging
    logger = setup_logger()
    logger.info("Starting VoiceTyping application")
    
    # Khởi tạo ứng dụng
    app = QApplication(sys.argv)
    
    # Khởi tạo controller
    docs_controller = DocsController()
    
    # Khởi tạo giao diện
    window = MainWindow(docs_controller)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()