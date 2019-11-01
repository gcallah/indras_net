"""
"""
import json
import random
from unittest import TestCase, main, skip

from flask_restplus import Resource

from APIServer.model_creator_api import get_model_creator
from APIServer.api_utils import  ENDPOINT_DESCR

class TestModelCreator(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_model_creator(self):
        ret_dict = get_model_creator()
        self.assertTrue(ENDPOINT_DESCR in ret_dict)

if __name__ == "__main__":
    main()
