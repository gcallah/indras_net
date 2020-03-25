"""
"""
import json
from unittest import TestCase, main, skip

from APIServer.props_api import get_props, put_props
from APIServer.api_utils import ERROR

BASIC_MODEL_ID = 0
BAD_MODEL_ID = -999
# indra_dir = os.getenv("INDRA_HOME", "/home/indrasnet/indras_net")


class TestPropsAPI(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_props(self):
        """
        See if props can be gotten!
        We will try both the error case and a good case.
        """
        ret = get_props(BAD_MODEL_ID, "nonsense")
        self.assertTrue(ERROR in ret)

if __name__ == "__main__":
    main()
