# -*- coding: utf-8 -*-

from .context import clianet 

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        clianet.core.hello()


if __name__ == '__main__':
    unittest.main()
