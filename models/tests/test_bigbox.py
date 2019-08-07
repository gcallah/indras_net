from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.space import Space
from indra.env import Env
from models.bigbox import create_consumer, create_bb, create_mp, set_up
from models.bigbox import calc_util, transaction, town_action
from models.bigbox import bb_store, consumer_action, mp_action, bb_action
from models.bigbox import MP_PREF, RADIUS, CONSUMER_INDX, get_store_census
from models.bigbox import BB_INDX, MP_INDX, mp_stores
import models.bigbox as bb

TEST_WIDTH=4
TEST_HEIGHT=4

def print_sep():
    print("________________________", flush=True)

class BigBoxTestCase(TestCase):
	def setup(self):
		"""
		set up test environment
		"""
		(bb.town, bb.groups) = set_up()
		pass

	def tearDown(self):
		bb.town = None
		bb.groups = None
		pass

	def test_calc_util(self):
		"""
		Create a big box agent
		Calculate the utility of the big box
		Test if the utility is bounded between 0.0 and 1.0
		"""
		a = bb.create_bb("Big box"+str(0))
		util = bb.calc_util(a)
		self.assertLess(util, 1.0)
		self.assertGreater(util, 0.0)
	

	def test_transaction(self):
		"""
		Create a big box agent
		Create a consumer agent
		Transact the money from consumer to big box
		Check if big box dies when its capital is below 0
		"""
		a = bb.create_bb("Big box" + str(0))
		b = bb.create_consumer("Consumer" + str(0))
		spending_power = b.attrs["spending power"]
		bb.transaction(a,b)
		self.assertEqual(a.attrs["capital"],480 + spending_power)
		self.assertEqual(a.attrs["inventory"][1], 89)
		a.attrs["inventory"][1] -= 87
		bb.transaction(a,b)
		self.assertEqual(a.attrs["inventory"][1], 91)
		self.assertEqual(a.attrs["capital"], 480 + (2 * spending_power) - 25)
		while a.attrs["capital"] > -1 * spending_power:
			a.attrs["capital"] -= (a.attrs["fixed expense"])
		bb.transaction(a,b)
		self.assertEqual(a.active, False)


	def test_create_consumer(self):
		"""
		Create a consumer agent
		"""
		bob = bb.create_consumer("Consumer"+str(0))
		self.assertEqual(len(bob.attrs), 3)


	def test_create_mp(self):
		"""
		Create a mom and pop agent
		"""
		mp = bb.create_mp("Mom and pop: Books", 0)
		self.assertEqual(len(mp.attrs), 5)


	def test_create_bb(self):
		"""
		Create a big box agent
		"""
		bigBox = bb.create_bb("Big Box"+str(0))
		self.assertEqual(len(bigBox.attrs), 5)

	
	def test_mp_action(self):
		"""
		Test if the action of mom and pop returns True
		"""
		mp = bb.create_mp("Mom and pop: Books", 0)
		self.assertEqual(True, bb.mp_action(mp))


	def test_bb_action(self):
		"""
		Test if the action of big box returns True
		"""
		bigBox = bb.create_bb("Big Box" + str(0))
		self.assertEqual(True, bb.bb_action(bigBox))


	def test_consumer_action(self):
		"""
		Test of the action of consumer returns False
		"""
		bob = bb.create_consumer("Consumer" + str(0))
		self.assertEqual(False, bb.consumer_action(bob))
