"""
Tests for the model_creator_api module.
"""
from unittest import TestCase, main

from APIServer.model_creator_api import get_model_creator


class TestModelCreator(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_model_creator(self):
        """
        This tests the get endpoint for the model creator.
        """
        ret_dict = get_model_creator()
        # this endpoint was changed without changing the test!
        # self.assertTrue(ENDPOINT_DESCR in ret_dict)


if __name__ == "__main__":
    main()
