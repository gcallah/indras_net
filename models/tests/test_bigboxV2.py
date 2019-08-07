from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.space import Space
from indra.env import Env
from models.bigboxV2 import create_consumer, create_bb, create_mp, set_up
from models.bigboxV2 import calc_util, transaction, town_action
from models.bigboxV2 import consumer_action, mp_action, bb_action, bb_capital
from models.bigboxV2 import MP_PREF, RADIUS, CONSUMER_INDX, groups
from models.bigboxV2 import BB_INDX, sells_good, get_util, MULTIPLIER
import models.bigboxV2 as bb2

TEST_WIDTH=4
TEST_HEIGHT=4

def print_sep():
    print("________________________", flush=True)

class BigBoxV2TestCase(TestCase):
	def setup(self):
		"""
		set up test environment
		"""
		(bb2.town, bb2.groups) = set_up()
		pass

	def tearDown(self):
		bb2.town = None
		bb2.groups = None
		pass

	def test_calc_util(self):
		"""
		Create a big box agent
		Calculate the utility of the big box
		Test if the utility is bounded between 0.0 and 1.0
		"""
		a = bb2.create_mp("Bookshop", 0)
		util = bb2.calc_util(a)
		self.assertLess(util, 1.0)
		self.assertGreater(util, 0.0)


	def test_transaction(self):
		"""
		Create a big box agent
		Create a consumer agent
		Transact the money from consumer to big box
		"""
		a = bb2.create_mp("Bookshop" , 1)
		b = bb2.create_consumer("Consumer", 0)
		spending_power = b["spending power"]
		capital = a["capital"]
		bb2.transaction(a,b)
		self.assertEqual(a["capital"],capital + spending_power)


	def test_create_consumer(self):
		"""
		Create a consumer agent
		"""
		bob = bb2.create_consumer("Consumer", 1)
		self.assertEqual(len(bob.attrs), 3)


	def test_create_mp(self):
		"""
		Create a mom and pop agent
		"""
		mp = bb2.create_mp("Bookshop" , 1)
		self.assertEqual(len(mp.attrs), 2)


	def test_create_bb(self):
		"""
		Create a big box agent
		"""
		bigBox = bb2.create_bb("Big Box")
		self.assertEqual(len(bigBox.attrs), 2)

	
	def test_mp_action(self):
		self.tearDown()
		self.setup()
		mp = bb2.create_mp("Bookshop" , 1)
		expense = mp["expense"]
		capital = mp["capital"]
		self.assertEqual(True, bb2.mp_action(mp))
		bb2.mp_action(mp)
		self.assertEqual(mp["capital"], capital - 2*expense)


	def test_bb_action(self):
		bigbox = bb2.create_bb("BigBox")
		expense = bigbox["expense"]
		capital = bigbox["capital"]
		self.assertEqual(True, bb2.bb_action(bigbox))
		bb2.bb_action(bigbox)
		self.assertEqual(bigbox["capital"], capital - 2*expense)
	

	# def test_consumer_action(self):
	# 	mp = bb2.create_mp("Bookshop", 1)
	# 	consumer = bb2.create_consumer("Consumer", 0)
	# 	consumer["item needed"] = "Bookshop"
	# 	spending = consumer["spending power"]
	# 	capital = mp["capital"]
	# 	self.assertEqual(bb2.consumer_action(consumer), False)
	# 	bb2.consumer_action(consumer)
	# 	self.assertEqual(mp["capital"], capital + spending)


	# def test_sells_good(self):
	# 	bigbox = bb2.create_bb("BigBox")
	# 	consumer = bb2.create_consumer("Consumer", 1)
	# 	self.assertEqual(bb2.sells_good(bigbox, consumer), True)
	# 	mp = bb2.create_mp("Bookshop" , 1)
	# 	consumer["item needed"] = "Bookshop"
	# 	self.assertEqual(bb2.sells_good(mp, consumer), True)
	# 	consumer["item needed"] = "Restaurant"
	# 	self.assertEqual(bb2.sells_good(mp, consumer), False)
	

	# def test_get_util(self):
	# 	bigbox = bb2.create_bb("BigBox")
	# 	mp = bb2.create_mp("Bookshop", 1)
	# 	bb_util = bb2.get_util(bigbox)
	# 	mp_util = bb2.get_util(mp)
	# 	self.assertLess(bb_util, 1.0)
	# 	self.assertGreater(bb_util, 0.0)
	# 	self.assertLess(mp_util, 1.1)
	# 	self.assertGreater(mp_util, 0.1)
