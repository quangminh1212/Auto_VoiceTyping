import pyautogui
import time
import pyperclip
import keyboard
import logging
import platform
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from backend.recognizer import UTF8FileHandler

# Cấu hình logging với mã hóa UTF-8
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        UTF8FileHandler("voicetyping.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("InputController")

class InputController(QObject):
    alt_pressed = pyqtSignal(bool)
    text_typed = pyqtSignal(bool, str)  # Tín hiệu mới: thành công, văn bản

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_alt_state)
        self.timer.start(10)  # Kiểm tra mỗi 10ms
        self.last_alt_state = False
        self.is_typing = False
        self.clipboard_method_failed = False  # Theo dõi nếu phương pháp clipboard thất bại
        self.os_name = platform.system()
        logger.info(f"InputController khởi tạo trên hệ điều hành: {self.os_name}")

    def type_text(self, text):
        if not text or text.isspace():
            logger.warning("Văn bản trống hoặc chỉ chứa khoảng trắng, bỏ qua")
            return
            
        if self.is_typing:
            logger.warning("Đang trong quá trình gõ, bỏ qua yêu cầu mới")
            return
            
        logger.info(f"Chuẩn bị nhập văn bản: '{text}'")
        self.is_typing = True
        # Đợi lâu hơn để đảm bảo phím Alt được nhả ra
        QTimer.singleShot(300, lambda: self._type_text(text))

    def _type_text(self, text):
        try:
            # Thử phương pháp clipboard trước nếu chưa thất bại trước đó
            if not self.clipboard_method_failed:
                success = self._type_with_clipboard(text)
                if not success:
                    logger.warning("Phương pháp clipboard thất bại, chuyển sang phương pháp gõ trực tiếp")
                    self.clipboard_method_failed = True
                    success = self._type_directly(text)
            else:
                # Sử dụng phương pháp gõ trực tiếp nếu clipboard đã thất bại trước đó
                success = self._type_directly(text)
                
            if success:
                logger.info(f"Đã nhập văn bản thành công: '{text}'")
                self.text_typed.emit(True, text)
            else:
                logger.error(f"Không thể nhập văn bản: '{text}'")
                self.text_typed.emit(False, text)
        except Exception as e:
            logger.exception(f"Lỗi khi nhập văn bản: {e}")
            self.text_typed.emit(False, text)
        finally:
            self.is_typing = False

    def _type_with_clipboard(self, text):
        """Sử dụng clipboard để nhập văn bản."""
        try:
            # Lưu nội dung clipboard hiện tại
            original_clipboard = pyperclip.paste()
            logger.debug(f"Nội dung clipboard gốc: '{original_clipboard[:20]}...'")
            
            # Sao chép văn bản mới vào clipboard
            pyperclip.copy(text)
            time.sleep(0.1)  # Đợi để đảm bảo văn bản đã được sao chép
            
            # Kiểm tra xem văn bản đã được sao chép vào clipboard chưa
            clipboard_content = pyperclip.paste()
            if clipboard_content != text:
                logger.error(f"Không thể sao chép văn bản vào clipboard: '{text}' != '{clipboard_content}'")
                return False
                
            # Đảm bảo Alt không được nhấn (có thể vẫn đang được nhấn nếu người dùng chưa nhả)
            while keyboard.is_pressed('alt'):
                logger.debug("Đang đợi phím Alt được nhả...")
                time.sleep(0.1)
                
            # Dán văn bản vào vị trí con trỏ hiện tại (vẫn giữ nguyên Ctrl+V)
            logger.debug("Đang thực hiện tổ hợp phím Ctrl+V")
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2)  # Đợi để đảm bảo văn bản đã được dán
            
            # Khôi phục clipboard gốc
            if original_clipboard:
                pyperclip.copy(original_clipboard)
                
            return True
        except Exception as e:
            logger.exception(f"Lỗi khi sử dụng phương pháp clipboard: {e}")
            return False

    def _type_directly(self, text):
        """Gõ văn bản trực tiếp không sử dụng clipboard."""
        try:
            logger.info("Đang sử dụng phương pháp gõ trực tiếp")
            # Đảm bảo Alt không được nhấn
            while keyboard.is_pressed('alt'):
                logger.debug("Đang đợi phím Alt được nhả...")
                time.sleep(0.1)
                
            # Gõ trực tiếp từng ký tự
            logger.debug(f"Bắt đầu gõ trực tiếp: '{text}'")
            pyautogui.write(text, interval=0.01)  # Gõ với tốc độ vừa phải
            return True
        except Exception as e:
            logger.exception(f"Lỗi khi sử dụng phương pháp gõ trực tiếp: {e}")
            return False

    def check_alt_state(self):
        try:
            is_pressed = keyboard.is_pressed('alt')
            if is_pressed != self.last_alt_state:
                self.last_alt_state = is_pressed
                logger.debug(f"Trạng thái phím Alt thay đổi: {is_pressed}")
                self.alt_pressed.emit(is_pressed)
        except Exception as e:
            logger.exception(f"Lỗi khi kiểm tra trạng thái phím Alt: {e}")

