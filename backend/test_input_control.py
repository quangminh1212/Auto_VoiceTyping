import unittest
from unittest.mock import patch
from controller import InputController

class TestInputController(unittest.TestCase):
    def setUp(self):
        self.controller = InputController()

    @patch('pyautogui.typewrite')
    @patch('pyautogui.click')
    @patch('pyautogui.position')
    def test_type_text(self, mock_position, mock_click, mock_typewrite):
        mock_position.return_value = (100, 100)
        self.controller.type_text("Xin chào thế giới")
        mock_click.assert_called_once_with((100, 100))
        mock_typewrite.assert_called_once_with("Xin chào thế giới")

if __name__ == '__main__':
    unittest.main()
