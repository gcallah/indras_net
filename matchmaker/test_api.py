#!/usr/bin/env python3
"""
Test our API functions.
"""

from unittest import TestCase, main

from indra.api import get_agent, TEST_GOAL


class APITestCase(TestCase):

    def test_get_agent(self):
        answer = get_agent("dummy_id")
        print(answer)
        self.assertTrue(answer["goal"] == TEST_GOAL)
#        self.assertTrue(error.startswith(INVALID_INSTR))

if __name__ == '__main__':
    main()
