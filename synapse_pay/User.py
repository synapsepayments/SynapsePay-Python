"""Summary"""
import APIClient

class User(object):
	"""Summary"""
	def __init__(self, **kwargs):
		"""Summary
		
		Args:
		    **kwargs: Description
		"""
		self.json = kwargs.get('json')
		self.client = kwargs.get('client')
		self.fingerprint = kwargs.get('fingerprint')
		self.ip_address = kwargs.get('ip_address')
		self.oauth_key = self.get_oauth_key()

	def get_oauth_key(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		payload = {
			'refresh_token': self.json['refresh_token']
		}
		path = 'api/3/oauth/{0}'.format(self.json['_id'])
		response = APIClient.post(
			client=self.client,
			fingerprint=self.fingerprint,
			path=path,
			payload=payload,
			ip_address=self.ip_address
		)
		return response['oauth_key']

	def update(self, **kwargs):
		"""Summary
		
		Args:
		    **kwargs: Description
		
		Returns:
		    TYPE: Description
		"""
		response = APIClient.patch(
			client=self.client,
			url=self.json['_links']['self']['href'],
			fingerprint=self.fingerprint,
			oauth_key=self.oauth_key,
			payload=kwargs.get('payload'),
			ip_address=self.ip_address
		)
		self.json = response
		return response

	def add_doc(self, **kwargs):
		"""Summary
		
		Args:
		    **kwargs: Description
		
		Returns:
		    TYPE: Description
		"""
		response = APIClient.patch(
			client=self.client,
			url=self.json['_links']['self']['href'],
			oauth_key=self.oauth_key,
			fingerprint=self.fingerprint,
			payload=kwargs.get('payload'),
			ip_address=self.ip_address
		)
		if response.get('http_code','200') != '202':
			self.json = response
		return response


	def answer_kba(self, **kwargs):
		"""Summary
		
		Args:
		    **kwargs: Description
		
		Returns:
		    TYPE: Description
		"""
		response = APIClient.patch(
			client=self.client,
			oauth_key=self.oauth_key,
			url=self.json['_links']['self']['href'],
			fingerprint=self.fingerprint,
			payload=kwargs.get('payload'),
			ip_address=self.ip_address
		)
		self.json = response
		return response
