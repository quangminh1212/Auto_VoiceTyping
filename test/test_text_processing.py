import unittest
from processor import TextProcessor

class TestTextProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = TextProcessor()

    def test_process_text(self):
        input_text = "xin chào thế giới. đây là một bài kiểm tra."
        expected_output = "Xin chào thế giới. Đây là một bài kiểm tra."
        result = self.processor.process_text(input_text)
        self.assertEqual(result, expected_output)

    def test_process_text_single_sentence(self):
        input_text = "xin chào thế giới"
        expected_output = "Xin chào thế giới"
        result = self.processor.process_text(input_text)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
