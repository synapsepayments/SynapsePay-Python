"""Summary"""
import unittest
from Helpers import *
from synapse_pay import Clients, Users, Helpers

class UserTestCases(unittest.TestCase):
	"""Summary"""
	def setUp(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		self.file_url = 'https://s3.amazonaws.com/synapse_django/static_assets/marketing/images/synapse_dark.png'
		self.client = Clients(
			client_id=CLIENT_ID,
			client_secret=CLIENT_SECRET,
			is_production=False
		)
		

	def get_question_set(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		user = self.create_user()
		doc_payload = {
			"doc":{
				"birth_day":4,
				"birth_month":2,
				"birth_year":1940,
				"name_first":"John",
				"name_last":"doe",
				"address_street1":"1 Infinite Loop",
				"address_postal_code":"95014",
				"address_country_code":"US",
				"document_value":"3333",
				"document_type":"SSN"
			}
		}
		return user.add_doc(payload=doc_payload), user


	def create_user(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
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
		return Users.create(
			client=self.client,
			payload=create_payload,
			fingerprint=FINGERPRINT,
			ip_address=IP_ADDRESS
		)


	def test_add_doc(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		doc_response, user = self.get_question_set()
		self.assertTrue(doc_response['success'])


	def test_answer_kba(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		doc_response, user = self.get_question_set()
		kba_payload = {
			"doc":{
				"question_set_id":doc_response['question_set']['id'],
				"answers":[
					{"question_id": 1, "answer_id": 1},
					{"question_id": 2, "answer_id": 1},
					{"question_id": 3, "answer_id": 1},
					{"question_id": 4, "answer_id": 1},
					{"question_id": 5, "answer_id": 1}
				]
			}
		}
		kba_response = user.answer_kba(payload=kba_payload)
		self.assertEqual(kba_response['permission'], 'RECEIVE')

	def test_attach_file(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		base_64 = Helpers.url_to_base64(url=self.file_url)
		file_payload = {
			'doc':{
				'attachment': base_64
			}
		}
		user = self.create_user()
		attach_response = user.update(payload=file_payload)
		self.assertTrue(not attach_response.has_key('success'))

if __name__ == '__main__':
    unittest.main()
    