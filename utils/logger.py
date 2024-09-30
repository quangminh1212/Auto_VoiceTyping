import logging
import os

def setup_logger():
    logger = logging.getLogger('voicetyping')
    logger.setLevel(logging.DEBUG)

    # Tạo handler cho console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Tạo handler cho file
    if not os.path.exists('logs'):
        os.makedirs('logs')
    file_handler = logging.FileHandler('logs/voicetyping.log')
    file_handler.setLevel(logging.DEBUG)

    # Tạo formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Thêm handlers vào logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger