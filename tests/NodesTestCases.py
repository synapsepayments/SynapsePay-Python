import unittest
from synapse_pay.Clients import Clients
import synapse_pay.Users as Users
import synapse_pay.Nodes as Nodes
from synapse_pay.APIClient import APIError
from Helpers import *

class NodesTestCases(unittest.TestCase):

	def setUp(self):
		client = Clients(
			client_id=CLIENT_ID,
			client_secret=CLIENT_SECRET,
			is_production=False,
			ip_address=IP_ADDRESS
		)
		create_payload = {
			"logins": [
				{
					"email": "pythonTest@synapsepay.com",
					"password": "test1234",
					"read_only":False
				}
			],
			"phone_numbers": [
				"901.111.1111"
			],
			"legal_names": [
				"PYTHON TEST USER"
			],
			"extra": {
				"note": "Interesting user",
				"supp_id": "122eddfgbeafrfvbbb",
				"is_business": False
			}
		}
		self.user = Users.create(
			payload=create_payload,
			client=client,
			fingerprint=FINGERPRINT
		)
		self.node_id = Nodes.get(user=self.user, client=client)['nodes'][0]['_id']
		

	def test_create_success(self):
		node_payload = {
			"type":"ACH-US",
			"info":{
				"nickname":"Python Library Savings Account",
				"name_on_account":"Python Library",
				"account_num":"72347235423",
				"routing_num":"051000017",
				"type":"PERSONAL",
				"class":"CHECKING"
			},
			"extra":{
				"supp_id":"123sa"
			}
		}
		nodes = Nodes.create(
			payload=node_payload,
			user=self.user
		)
		self.assertTrue(nodes[0].json != None)

	def test_create_error(self):
		node_payload = {
			"info":{
				"nickname":"Python Library Savings Account",
				"name_on_account":"Python Library",
				"account_num":"72347235423",
				"routing_num":"051000017",
				"type":"PERSONAL",
				"class":"CHECKING"
			},
			"extra":{
				"supp_id":"123sa"
			}
		}
		try:
			node = Nodes.create(
				payload=node_payload,
				user=self.user
			)
			self.assertTrue(node == None)
		except APIError as error:
			self.assertTrue(error != None)

	def test_get_success(self):
		node = Nodes.get(user=self.user, _id=self.node_id)
		self.assertTrue(node.json != None)

	def test_get_error(self):
		try:
			node = Nodes.get(user=None, _id=self.node_id)
			self.assertTrue(node != None)
		except AttributeError:
			self.assertTrue(True)

	def test_multi_get_success(self):
		nodes = Nodes.get(user=self.user)
		self.assertTrue(len(nodes['nodes']) > 0)

	def test_multi_get_error(self):
		try:
			nodes = Nodes.get(user=None)
			self.assertTrue(len(nodes['nodes']) < 1)
		except AttributeError:
			self.assertTrue(True)
			
if __name__ == '__main__':
    unittest.main()
    