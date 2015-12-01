"""Summary"""
import APIClient

class Transaction(object):
	"""Summary"""
	def __init__(self, **kwargs):
		"""Object representation of a synapse transaction.
		
		Args:
		    **kwargs:	json - the json representation of the synapse transaction
		    			node - the from node of the transaction
		"""
		self.json = kwargs.get('json')
		self.node = kwargs.get('node')


	def update(self, **kwargs):
		"""Updates the transaction with a given comment.
		
		Args:
		    **kwargs:	payload - json object to PATCH the transaction with
		
		Returns:
		    Transaction:	The updated transaction
		"""
		response = APIClient.patch(
			client=self.node.user.client,
			oauth_key=self.node.user.oauth_key,
			fingerprint=self.node.user.fingerprint,
			payload=kwargs.get('payload'),
			url=self.json['_links']['self']['href'],
			ip_address=self.node.user.ip_address
		)
		self.json = response['trans']
		return response


	def delete(self):
		"""Cancels the transaction
		
		Returns:
		    bool: True if transaction successfully canceled or False otherwise
		"""
		response = APIClient.delete(
			client=self.node.user.client,
			oauth_key=self.node.user.oauth_key,
			fingerprint=self.node.user.fingerprint,
			url=self.json['_links']['self']['href'],
			ip_address=self.node.user.ip_address
		)
		del self
		return response['recent_status']['status'] == u'CANCELED'
