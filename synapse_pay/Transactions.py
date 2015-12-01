"""Summary"""
import APIClient
from Transaction import Transaction

BASE_PATH = 'api/3/users/{0}/nodes/{1}/trans'

def create(**kwargs):
	"""Summary
	
	Args:
	    **kwargs: Description
	
	Returns:
	    TYPE: Description
	"""
	node = kwargs.get('node')
	path = BASE_PATH.format(node.user.json['_id'], node.json['_id'])
	response = APIClient.post(
		client=node.user.client,
		oauth_key=node.user.oauth_key,
		fingerprint=node.user.fingerprint,
		path=path,
		payload=kwargs.get('payload')
	)
	return Transaction(json=response, node=node)

def get(**kwargs):
	"""Summary
	
	Args:
	    **kwargs: Description
	
	Returns:
	    TYPE: Description
	"""
	_id = kwargs.get('_id')
	node = kwargs.get('node')
	path = BASE_PATH.format(node.user.json['_id'], node.json['_id'])
	if _id:
		path += '/{0}'.format(_id)
		response = APIClient.get(
			client=node.user.client,
			oauth_key=node.user.oauth_key,
			fingerprint=node.user.fingerprint,
			path=path,
			ip_address=node.user.ip_address
		)
		return Transaction(json=response, node=node)
	else:
		query_params = {
			'type': kwargs.get('type'),
			'page': kwargs.get('page', 1),
			'per_page': kwargs.get('per_page', 20)
		}
		response = APIClient.get(
			client=node.user.client,
			oauth_key=node.user.oauth_key,
			fingerprint=node.user.fingerprint,
			path=path,
			ip_address=node.user.ip_address,
			query_params=query_params
		)
		return response
