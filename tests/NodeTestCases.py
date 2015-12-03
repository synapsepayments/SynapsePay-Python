
import unittest
from synapse_pay import Clients, Users, Nodes
from Helpers import *

class NodeTestCases(unittest.TestCase):

	def setUp(self):
		client = Clients(
			fingerprint=FINGERPRINT,
			client_id=CLIENT_ID,
			client_secret=CLIENT_SECRET,
			is_production=False
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
			fingerprint=FINGERPRINT,
			client=client,
			ip_address=IP_ADDRESS
		)
		self.node = Nodes.get(user=self.user, client=client)
		
		
	def test_delete_success(self):
		node_payload = {
			"type":"SYNAPSE-US",
		    "info":{
		      "nickname":"My Synapse Wallet"
		    },
		    "extra":{
		      "supp_id":"123sa"
		    }
		}
		node = Nodes.create(user=self.user, payload=node_payload)[0]
		result = node.delete()
		self.assertTrue(result)

	def test_update_success(self):
		node_payload = {
			"type":"ACH-US",
			"info":{
				"nickname":"Savings Account",
				"account_num":"123567444",
				"routing_num":"051000017",
				"type":"PERSONAL",
				"class":"CHECKING"
			},
			"extra":{
				"supp_id":"123sa"
			}
		}
		node = Nodes.create(user=self.user, payload=node_payload)[0]
		self.assertTrue(node.json['allowed'] == 'CREDIT')
		verify_payload = {
			"micro":[0.1, 0.1]
		}
		node.update(payload=verify_payload)
		self.assertTrue(node.json['allowed'] != 'CREDIT')


if __name__ == '__main__':
    unittest.main()
    