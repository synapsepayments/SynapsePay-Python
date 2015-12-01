"""Summary"""
import logging

class Clients(object):
	"""Summary"""
	def __init__(self, **kwargs):
		"""Constructor
		
		Args:
		    **kwargs:	client_id - your SynapsePay client_id
		    			client_secret - your SynapsePay client_secret
		    			is_production - boolean to ping either sandbox or is_production
		    			log_requests - boolean on whether to log every http request
		"""
		self.client_id = kwargs.get('client_id')
		self.client_secret = kwargs.get('client_secret')
		self.is_production = kwargs.get('is_production')
		self.log_requests = kwargs.get('log_requests', False)
		if self.log_requests:
			start_logging()


	def get_client_id(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		return self.client_id

	def get_base_path(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		if self.is_production:
			return 'https://synapsepay.com/'
		else:
			return 'https://sandbox.synapsepay.com/'

	def get_client_secret(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		return self.client_secret


	def set_client_id(self, client_id):
		"""Summary
		
		Args:
		    client_id (TYPE): Description
		
		Returns:
		    TYPE: Description
		"""
		self.client_id = client_id

	def set_client_secret(self, client_secret):
		"""Summary
		
		Args:
		    client_secret (TYPE): Description
		
		Returns:
		    TYPE: Description
		"""
		self.client_secret = client_secret


def start_logging():
	"""Summary
	
	Returns:
	    TYPE: Description
	"""
	try:
		import http.client as http_client
	except ImportError:
		# Python 2
		import httplib as http_client
	http_client.HTTPConnection.debuglevel = 1
	logging.basicConfig() 
	logging.getLogger().setLevel(logging.DEBUG)
	requests_log = logging.getLogger("requests.packages.urllib3")
	requests_log.setLevel(logging.DEBUG)
	requests_log.propagate = True
