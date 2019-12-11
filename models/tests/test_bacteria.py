"""
This is the test suite for space.py.
"""

from unittest import TestCase, main

from propargs.propargs import PropArgs

import models.bacteria as ba
from indra.composite import Composite
from models.bacteria import set_up, create_bacterium, create_toxin, \
    create_nutrient, bacterium_action, calc_nutrient, \
    calc_toxin

TEST_BAC_NUM = 3
TEST_TOX_NUM = 3
TEST_NUTRI_NUM = 3


class BacteriaTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('bacteria_props',
                                        ds_file='props/bacteria.props.json')
        (ba.petri_dish, ba.toxins, ba.nutrients, ba.bacteria) = set_up()
        self.toxin = create_toxin("Toxins", TEST_TOX_NUM, self.pa)
        self.nutrient = create_nutrient("Nutrients", TEST_NUTRI_NUM, self.pa)
        self.bacterium = create_bacterium("Bacteria", TEST_BAC_NUM, self.pa)

    def tearDown(self):
        self.test_toxins = None
        self.test_nutrients = None
        self.test_bacteria = None

    def test_create_toxin(self):
        """
         Test to see if toxin is created
        """
        new_toxin = create_toxin("Toxins", 0, self.pa)
        self.assertTrue(new_toxin["max_move"] >= 0)

    def test_create_nutrient(self):
        """
        Test to see if nutrient is created
        """
        new_nutrient = create_toxin("Nutrients", 0, self.pa)
        self.assertTrue(new_nutrient["max_move"] >= 0)

    def test_create_bacterium(self):
        """
        Test to see if bacterium is created
        """
        new_bacterium = create_bacterium("Bacteria", 0, self.pa)
        self.assertTrue(new_bacterium["prev_toxicity"] is None)
        self.assertTrue(new_bacterium["prev_nutricity"] is None)
        self.assertTrue(new_bacterium["angle"] is None)

    def test_calc_toxin(self):
        '''
        Test if we get proper toxin level
        '''
        toxins_group = Composite("Toxins")
        bacterium = create_bacterium("Bacteria", 0, self.pa)
        for i in range(TEST_TOX_NUM):
            toxins_group += create_toxin("Toxins", i, self.pa)
        toxin_strength = calc_toxin(toxins_group, bacterium)
        self.assertTrue(toxin_strength < 0)

    def test_calc_nutrient(self):
        '''
        Test if we get proper nutrient level
        '''
        nutrients_group = Composite("nutrients")
        bacterium = create_bacterium("Bacteria", 0, self.pa)
        for i in range(TEST_NUTRI_NUM):
            nutrients_group += create_nutrient("nutrients", i, self.pa)
        nutrient_strength = calc_nutrient(nutrients_group, bacterium)
        self.assertTrue(nutrient_strength > 0)

    def test_bacterium_action(self):
        '''
        Test if the previous nutricity and toxicity of the bacterium 
        change when the function is called
        '''
        bacterium = create_bacterium("Bacteria", 0, self.pa)
        bacterium["prev_toxicity"] = 0
        bacterium["prev_nutricity"] = 0
        bacterium_action(bacterium)
        self.assertTrue(bacterium["prev_nutricity"] > 0)
        self.assertTrue(bacterium["prev_toxicity"] < 0)

    if __name__ == '__main__':
        main()
