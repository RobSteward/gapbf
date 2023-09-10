import unittest
from unittest.mock import patch
from PathHandler import ADBHandler, config

class TestADBHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ADBHandler(config)

    @patch('subprocess.run')
    def test_try_path_success(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = config.stdout_success[0]
        mock_run.return_value.stderr = ""
        path = "test_path"
        result = self.handler.try_path(path)
        self.assertTrue(result)

    @patch('subprocess.run')
    def test_try_path_failure(self, mock_run):
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = config.stdout_normal
        mock_run.return_value.stderr = "error"
        path = "test_path"
        result = self.handler.try_path(path)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()