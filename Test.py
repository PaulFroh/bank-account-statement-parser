import unittest

import config_helper

class ExampleTest(unittest.TestCase):

    def test_example(self):
        self.assertEqual(1,1, "Should be 1")


if __name__ == '__main__':
    unittest.main()