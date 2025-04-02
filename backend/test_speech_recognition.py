import unittest
from unittest.mock import patch
from recognizer import SpeechRecognizer

class TestSpeechRecognizer(unittest.TestCase):
    def setUp(self):
        self.recognizer = SpeechRecognizer()

    @patch('speech_recognition.Recognizer.recognize_google')
    @patch('speech_recognition.Microphone')
    def test_recognize_speech(self, mock_microphone, mock_recognize_google):
        mock_recognize_google.return_value = "Xin chào thế giới"
        result = self.recognizer.recognize_speech()
        self.assertEqual(result, "Xin chào thế giới")

    @patch('speech_recognition.Recognizer.recognize_google')
    @patch('speech_recognition.Microphone')
    def test_recognize_speech_unknown_value(self, mock_microphone, mock_recognize_google):
        mock_recognize_google.side_effect = sr.UnknownValueError()
        result = self.recognizer.recognize_speech()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
