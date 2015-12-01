"""Summary"""
import APIClient
from Node import Node

BASE_PATH = 'api/3/users/{0}/nodes'


def get(**kwargs):
	"""Summary
	
	Args:
	    **kwargs: Description
	
	Returns:
	    TYPE: Description
	"""
	user = kwargs.get('user')
	_id = kwargs.get('_id')
	path = BASE_PATH.format(user.json['_id'])
	if _id:
		path += '/{0}'.format(_id)
		response = APIClient.get(
			client=user.client,
			oauth_key=user.oauth_key,
			fingerprint=user.fingerprint,
			path=path,
			ip_address=user.ip_address
		)
		return Node(json=response, user=user)
	else:
		query_params = {
			'type': kwargs.get('type'),
			'page': kwargs.get('page', 1),
			'per_page': kwargs.get('per_page', 20)
		}
		response = APIClient.get(
			client=user.client,
			oauth_key=user.oauth_key,
			fingerprint=user.fingerprint,
			path=path,
			query_params=query_params,
			ip_address=user.ip_address
		)
		return response

def create(**kwargs):
	"""Summary
	
	Args:
	    **kwargs: Description
	
	Returns:
	    TYPE: Description
	"""
	user = kwargs.get('user')
	path = BASE_PATH.format(user.json['_id'])
	response = APIClient.post(
		client=user.client,
		oauth_key=user.oauth_key,
		fingerprint=user.fingerprint,
		path=path,
		payload=kwargs.get('payload'),
		ip_address=user.ip_address
	)
	if 'mfa' in response:
		return response
	else:
		nodes = []
		for node in response['nodes']:
			nodes.append(Node(json=node, user=user))
		return nodes
