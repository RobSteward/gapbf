import unittest
from PathFinder import PathFinder
from PathHandler import PathHandler

class TestPathFinder(unittest.TestCase):
    def setUp(self):
        self.path_finder = PathFinder(10)
        self.path_finder.add_handler(PathHandler())

    def test_dfs(self):
        graph = {
            '1': ['2', '3'],
            '2': ['4', '5'],
            '3': ['6', '7'],
            '4': ['8', '9'],
            '5': ['10'],
            '6': [],
            '7': [],
            '8': [],
            '9': [],
            '10': []
        }
        neighbors = {
            '1': ['2', '3'],
            '2': ['4', '5'],
            '3': ['6', '7'],
            '4': ['8', '9'],
            '5': ['10'],
            '6': [],
            '7': [],
            '8': [],
            '9': [],
            '10': []
        }
        self.path_finder.dfs(graph, neighbors, path_min_len=2, path_max_len=5, path_prefix=['1'], path_suffix=['10'], excluded_nodes=['7'])
        # Assert that the PathHandler object has received the correct paths
        self.assertEqual(self.path_finder.handlers[0].paths, [['1', '2', '4', '8', '10'], ['1', '2', '4', '9', '10'], ['1', '2', '5', '10']])

    def test_add_handler(self):
        handler = PathHandler()
        self.path_finder.add_handler(handler)
        self.assertIn(handler, self.path_finder.handlers)

if __name__ == '__main__':
    unittest.main()