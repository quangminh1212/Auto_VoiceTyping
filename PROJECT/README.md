# VoiceTyping

Ứng dụng ghi âm và chuyển đổi giọng nói thành văn bản tích hợp với Google Docs.

## Cài đặt

1. Clone repository: 
PROJECT/
├── credentials/
│   └── client_secret.json  # File xác thực Google
├── logs/
├── auth/
│   └── google_auth.py
├── browser/
│   └── docs_controller.py
├── config/
│   └── config.py
├── state/
│   └── store.py
├── system/
│   └── interaction.py
├── text/
│   └── manager.py
├── ui/
│   └── main_window.py
├── utils/
│   ├── error_handler.py
│   ├── logger.py
│   └── security.py
├── main.py
└── requirements.txt