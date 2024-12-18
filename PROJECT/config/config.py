import os
from pathlib import Path

class Config:
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    LOGS_DIR = BASE_DIR / "logs"
    CREDENTIALS_DIR = BASE_DIR / "credentials"
    
    # Google Auth
    CLIENT_SECRET_FILE = CREDENTIALS_DIR / "client_secret.json"
    TOKEN_FILE = CREDENTIALS_DIR / "token.json"
    
    # App Settings
    APP_NAME = "VoiceTyping"
    WINDOW_WIDTH = 300
    WINDOW_HEIGHT = 400
    
    @classmethod
    def setup_directories(cls):
        os.makedirs(cls.LOGS_DIR, exist_ok=True)
        os.makedirs(cls.CREDENTIALS_DIR, exist_ok=True) 