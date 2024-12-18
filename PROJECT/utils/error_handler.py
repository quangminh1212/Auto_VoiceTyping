import sys
from functools import wraps
from PyQt6.QtWidgets import QMessageBox

def show_error_dialog(message, title="Lỗi"):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.exec()

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            show_error_dialog(str(e))
            return None
    return wrapper 