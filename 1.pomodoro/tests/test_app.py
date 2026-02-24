import unittest
from flask import Flask
from app import app

class PomodoroAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_content(self):
        response = self.app.get('/')
        self.assertIn(b'ポモドーロタイマー', response.data)
        self.assertIn(b'id="timer-minutes"', response.data)
        self.assertIn(b'id="start-btn"', response.data)

if __name__ == '__main__':
    unittest.main()
