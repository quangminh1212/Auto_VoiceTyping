import logging
import os
import sys

def setup_logger():
    logger = logging.getLogger('voicetyping')
    logger.setLevel(logging.DEBUG)

    # Tạo formatter hỗ trợ Unicode
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8')

    # Console handler với encoding utf-8
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler với encoding utf-8
    if not os.path.exists('logs'):
        os.makedirs('logs')
    file_handler = logging.FileHandler('logs/voicetyping.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger