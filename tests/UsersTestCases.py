import unittest
from Helpers import *
from synapse_pay.Clients import Clients
import synapse_pay.Users as Users
from synapse_pay.APIClient import APIError

class UsersTestCases(unittest.TestCase):
	
	def setUp(self):
		self.client = Clients(
			client_id=CLIENT_ID,
			client_secret=CLIENT_SECRET,
			is_production=False
		)
		
	def test_create_success(self):
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
		user = Users.create(
			payload=create_payload,
			fingerprint=FINGERPRINT,
			client=self.client,
			ip_address=IP_ADDRESS
		)
		self.assertTrue(user.json != None)
		self.assertTrue(user.oauth_key != None)

	def test_create_error(self):
		create_payload = {
			"logins": [
				{
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
		try:
			user = Users.create(
				payload=create_payload,
				fingerprint=FINGERPRINT,
				client=self.client
			)
			self.assertTrue(user.json == None)
			self.assertTrue(user.oauth_key == None)
		except APIError as error:
			self.assertTrue(error != None)

	def test_multi_get_success(self):
		users = Users.get(client=self.client)
		self.assertTrue(len(users) > 0)

	def test_multi_get_error(self):
		try:
			users = Users.get(client=None)
			self.assertTrue(False)
		except Exception as error:
			self.assertTrue(error != None)

	def test_get_success(self):
		user = Users.get(client=self.client, _id=USER_ID, fingerprint=FINGERPRINT, ip_address=IP_ADDRESS)
		self.assertTrue(user.json != None)
		self.assertTrue(user.oauth_key != None)
		self.assertTrue(user.ip_address == IP_ADDRESS)

	def test_get_error(self):
		user = Users.get(
			client=self.client,
			_id=VERIFIED_USER_ID,
			fingerprint=FINGERPRINT
		)
		self.assertTrue(user.json != None)
		self.assertTrue(user.oauth_key != None)
		self.assertTrue(user.ip_address == None)


if __name__ == '__main__':
    unittest.main()
    