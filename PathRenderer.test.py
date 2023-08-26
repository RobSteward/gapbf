# BEGIN: 1a2b3c4d5e6f
import unittest
from PathRenderer import render_path, render_path_steps

class TestPathRenderer(unittest.TestCase):
    def test_render_path(self):
        path = [0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5]
        expected_output = "\nPattern: 0-1-2-3-4-9-14-19-24-23-22-21-20-15-10-5\n●●●●●○○○○○\n○○○○●○○○○○\n○○○○●○○○○○\n○○○○●○○○○○\n○○○○●○○○○○\n"
        self.assertEqual(render_path(path), expected_output)

    def test_render_path_steps(self):
        path = [0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5]
        expected_output = "1 2 3 4 5 · · · · · \n· · · · 6 · · · · · \n· · · · 7 · · · · · \n· · · · 8 · · · · · \n· · · · 9 · · · · · \n"
        self.assertEqual(render_path_steps(path), expected_output)

if __name__ == '__main__':
    unittest.main()
# END: 1a2b3c4d5e6f