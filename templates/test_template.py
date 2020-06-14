"""
This is a template file for tests.
"""

from unittest import TestCase, main
import YOUR_MODULE as YM


class BasicTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main(self):
        self.assertEqual(YM.main(), 0)

    if __name__ == '__main__':
        main()
