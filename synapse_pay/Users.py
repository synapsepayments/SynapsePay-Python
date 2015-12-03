"""Summary

Attributes:
    USER_BASE_PATH (str): Description
"""
import APIClient
from User import User

BASE_PATH = 'api/3/users'

def get(**kwargs):
	"""Summary
	
	Args:
	    **kwargs: Description
	
	Returns:
	    TYPE: Description
	"""
	_id = kwargs.get('_id')
	client = kwargs.get('client')
	fingerprint = kwargs.get('fingerprint')
	ip_address = kwargs.get('ip_address')
	if _id:
		path = BASE_PATH + '/' + _id
		response = APIClient.get(
			client=client,
			path=path,
			fingerprint=fingerprint,
			ip_address=ip_address
		)
		return User(
			client=client,
			json=response,
			fingerprint=fingerprint,
			ip_address=ip_address
		)
	else:
		query_params = {
			'page': kwargs.get('page', 1),
			'per_page': kwargs.get('per_page', 20),
			'query': kwargs.get('query')
		}
		response = APIClient.get(
			client=client,
			path=BASE_PATH,
			fingerprint='',
			ip_address='',
			query_params=query_params
		)
		return response

def create(**kwargs):
	"""Summary
	
	Args:
	    **kwargs: Description
	
	Returns:
	    TYPE: Description
	"""
	client = kwargs.get('client')
	fingerprint = kwargs.get('fingerprint')
	ip_address = kwargs.get('ip_address')
	response = APIClient.post(
		client=client,
		fingerprint=fingerprint,
		payload=kwargs.get('payload'),
		ip_address=ip_address,
		path=BASE_PATH
	)
	return User(
		client=client,
		json=response,
		fingerprint=fingerprint,
		ip_address=ip_address
	)
