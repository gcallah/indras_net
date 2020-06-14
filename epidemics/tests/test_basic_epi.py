""" This is a template file for tests.  """ 
from unittest import TestCase, main
import epidemics.epidemic as be


class BasicTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    def testHealty(self):
	    saliou = be.create_person("Saliou",5)
	    self.assertEqual(be.is_healthy(saliou),1)
    def test_main(self):
        self.assertEqual(be.main(), 0)

if __name__ == '__main__':
     main()


