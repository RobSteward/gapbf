import unittest
import os
from Config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config_file = 'test_config.yaml'
        with open(self.config_file, 'w') as f:
            f.write('config:\n  grid_size: 10\n  path_min_length: 5\n  path_max_length: 20\n  path_prefix: "start"\n  path_suffix: "end"\n  excluded_nodes: [1, 2, 3]\n  attempt_delay: 0.5\n  test_path: "test"\n  outputstrings:\n    stdout_normal: "normal"\n    stdout_success: "success"\n    stdout_error: "error"\n  log_file_path: "log.txt"')

    def tearDown(self):
        os.remove(self.config_file)

    def test_load_config(self):
        handler = Config.(self.config_file)
        config = handler.load_config(self.config_file)
        self.assertEqual(config['config']['grid_size'], 10)
        self.assertEqual(config['config']['path_min_length'], 5)
        self.assertEqual(config['config']['path_max_length'], 20)
        self.assertEqual(config['config']['path_prefix'], 'start')
        self.assertEqual(config['config']['path_suffix'], 'end')
        self.assertEqual(config['config']['excluded_nodes'], [1, 2, 3])
        self.assertEqual(config['config']['attempt_delay'], 0.5)
        self.assertEqual(config['config']['test_path'], 'test')
        self.assertEqual(config['config']['outputstrings']['stdout_normal'], 'normal')
        self.assertEqual(config['config']['outputstrings']['stdout_success'], 'success')
        self.assertEqual(config['config']['outputstrings']['stdout_error'], 'error')
        self.assertEqual(config['config']['log_file_path'], 'log.txt')

    def test_get_value(self):
        handler = Config(self.config_file)
        self.assertEqual(handler.get_value('config.grid_size'), 10)
        self.assertEqual(handler.get_value('config.path_min_length'), 5)
        self.assertEqual(handler.get_value('config.path_max_length'), 20)
        self.assertEqual(handler.get_value('config.path_prefix'), 'start')
        self.assertEqual(handler.get_value('config.path_suffix'), 'end')
        self.assertEqual(handler.get_value('config.excluded_nodes'), [1, 2, 3])
        self.assertEqual(handler.get_value('config.attempt_delay'), 0.5)
        self.assertEqual(handler.get_value('config.test_path'), 'test')
        self.assertEqual(handler.get_value('config.outputstrings.stdout_normal'), 'normal')
        self.assertEqual(handler.get_value('config.outputstrings.stdout_success'), 'success')
        self.assertEqual(handler.get_value('config.outputstrings.stdout_error'), 'error')
        self.assertEqual(handler.get_value('config.log_file_path'), 'log.txt')

if __name__ == '__main__':
    unittest.main()