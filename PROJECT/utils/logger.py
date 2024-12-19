import logging
import os
import sys
import codecs

def setup_logger():
    logger = logging.getLogger('voicetyping')
    logger.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler(codecs.getwriter('utf-8')(sys.stdout.buffer))
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # File handler
    if not os.path.exists('logs'):
        os.makedirs('logs')
    file_handler = logging.FileHandler('logs/voicetyping.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger