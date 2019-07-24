from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.space import Space
from indra.env import Env
from models.bigbox import create_consumer, create_bb, create_mp, set_up
from models.bigbox import calc_util, transaction, town_action, pay_fixed_expenses
from models.bigbox import bb_store, consumer_action, mp_action, bb_action
from models.bigbox import MP_PREF, RADIUS, CONSUMER_INDX, get_store_census
from models.bigbox import BB_INDX, MP_INDX, mp_stores, town_action
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
		a= bb.create_bb("Big box"+str(0))
		util = bb.calc_util(a)
		self.assertLess(util, 1.0)
		self.assertGreater(util, 0.0)

	# def test_town_action(self):
	# 	"""
	# 	Create three composites and three agents with height
	# 	and width of 4. Test if twon_action works and see 
	# 	if transactions match.
	# 	"""
	# 	bigBox = Composite("blue")
	# 	consumer = Composite("gray")
	# 	mp = Composite("red")
	# 	bb.groups = []
	# 	bb.groups.append(bigBox)
	# 	bb.groups.append(consumer)
	# 	bb.groups.append(mp)
	# 	a = bb.create_bb("Big box"+str(0))
	# 	bb.groups[BB_INDX] += a
	# 	b = bb.create_consumer("Consumer"+str(0))
	# 	bb.groups[CONSUMER_INDX] += b
	# 	c = bb.create_mp(b.attrs["item needed"],0)
	# 	bb.groups[MP_INDX] += c
	# 	Test_town = Env("town for test", width=TEST_WIDTH, height=TEST_HEIGHT, members=bb.groups, action=bb.town_action)
	# 	bb.town_action(Test_town)
	# 	bb_util=bb.calc_util(a)
	# 	mp_util=bb.calc_util(c)+MP_PREF
	# 	max_util = max(bb_util, mp_util)
	# 	if bb_util > mp_util:
	# 		store_to_go = a
	# 	else:
	# 		store_to_go = c
	# 	bb.transaction(store_to_go,b)
	# 	if bb_util > mp_util:
	# 		self.assertEqual(a.attrs["capital"], 480+b.attrs["spending power"])
	# 	else:
	# 		self.assertEqual(a.attrs["capital"], 480)
	

	def test_transaction(self):
		"""
		Create a big box agent
		Create a consumer agent
		Transact the money from consumer to big box
		Check if big box dies when its capital is below 0
		"""
		a = bb.create_bb("Big box"+str(0))
		b = bb.create_consumer("Consumer"+str(0))
		spending_power = b.attrs["spending power"]
		bb.transaction(a,b)
		self.assertEqual(a.attrs["capital"],480+spending_power)
		self.assertEqual(a.attrs["inventory"][1], 89)
		a.attrs["inventory"][1]-=87
		bb.transaction(a,b)
		self.assertEqual(a.attrs["inventory"][1], 91)
		self.assertEqual(a.attrs["capital"], 480+2*spending_power-25)
		while a.attrs["capital"] > -1*spending_power:
			bb.pay_fixed_expenses(a)
		bb.transaction(a,b)
		self.assertEqual(a.active, False)


	def test_create_consumer(self):
		"""
		Create a consumer agent
		"""
		bob= bb.create_consumer("Consumer"+str(0))
		self.assertEqual(len(bob.attrs), 3)


	def test_create_mp(self):
		"""
		Create a mom and pop agent
		"""
		mp= bb.create_mp("books", 0)
		self.assertEqual(len(mp.attrs), 4)


	def test_create_bb(self):
		"""
		Create a big box agent
		"""
		bigBox = bb.create_bb("Big Box"+str(0))
		self.assertEqual(len(bigBox.attrs), 4)

	
	def test_pay_fixed_expenses(self):
		"""
		Create a big box agent
		Test if the fiexed expenses are deducted from the capital
		"""
		a = bb.create_bb("Big box"+str(0))
		bb.pay_fixed_expenses(a)
		self.assertEqual(a.attrs["capital"], 420)

	
	def test_mp_action(self):
		"""
		Test if the action of mom and pop returns True
		"""
		mp= bb.create_mp("books", 0)
		self.assertEqual(True, bb.mp_action(mp))


	def test_bb_action(self):
		"""
		Test if the action of big box returns True
		"""
		bigBox= bb.create_bb("Big Box"+str(0))
		self.assertEqual(True, bb.bb_action(bigBox))


	def test_consumer_action(self):
		"""
		Test of the action of consumer returns False
		"""
		bob= bb.create_consumer("Consumer"+str(0))
		self.assertEqual(False, bb.consumer_action(bob))





			

