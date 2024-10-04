import sys
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from main_window import MainWindow

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()

    def test_initial_state(self):
        self.assertEqual(self.window.windowTitle(), "VoiceTyping")
        self.assertEqual(self.window.status_label.text(), "Trạng thái: Chưa kích hoạt")
        self.assertTrue(self.window.start_button.isEnabled())
        self.assertFalse(self.window.stop_button.isEnabled())

    def test_start_recognition(self):
        QTest.mouseClick(self.window.start_button, Qt.LeftButton)
        self.assertEqual(self.window.status_label.text(), "Trạng thái: Đang nhận diện...")
        self.assertFalse(self.window.start_button.isEnabled())
        self.assertTrue(self.window.stop_button.isEnabled())

    def test_stop_recognition(self):
        QTest.mouseClick(self.window.start_button, Qt.LeftButton)
        QTest.mouseClick(self.window.stop_button, Qt.LeftButton)
        self.assertEqual(self.window.status_label.text(), "Trạng thái: Đã dừng")
        self.assertTrue(self.window.start_button.isEnabled())
        self.assertFalse(self.window.stop_button.isEnabled())

if __name__ == "__main__":
    unittest.main()
