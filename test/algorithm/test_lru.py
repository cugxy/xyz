import unittest

from xyz.algorithm.lru import LRUCache


class TestCaseLRU(unittest.TestCase):
    def test_lru0(self):
        lru = LRUCache(4)
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
