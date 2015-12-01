"""Node Object Representation of a SynapsePay Node."""
import APIClient

class Node(object):
	"""Node Object Representation of a SynapsePay Node."""


	def __init__(self, **kwargs):
		"""Constructor
		
		Args:
		    **kwargs:	json - the json representation of the object
		    			user - a synapse.User object that owns the node
		"""
		self.json = kwargs.get('json')
		self.user = kwargs.get('user')


	def update(self, **kwargs):
		"""Used to verify a micro-deposit Node.
		
		Args:
		    **kwargs:	payload - the json object to be sent to the server
		
		Returns:
		    Node:	self
		"""
		response = APIClient.patch(
			client=self.user.client,
			oauth_key=self.user.oauth_key,
			fingerprint=self.user.fingerprint,
			payload=kwargs.get('payload'),
			url=self.json['_links']['self']['href'],
			ip_address=self.user.ip_address
		)
		self.json = response
		return response


	def delete(self):
		"""Removes the syanpse node from the user.
		
		Returns:
		    bool: Whether the node was successfully deleted or not.
		"""
		APIClient.delete(
			client=self.user.client,
			oauth_key=self.user.oauth_key,
			fingerprint=self.user.fingerprint,
			url=self.json['_links']['self']['href'],
			ip_address=self.user.ip_address
		)
		del self
		return True
