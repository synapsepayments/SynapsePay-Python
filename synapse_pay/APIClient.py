"""Summary"""
import requests
import json


def get(**kwargs):
	"""Summary
	
	Args:
	    **kwargs: Description
	
	Returns:
	    TYPE: Description
	"""
	path = kwargs.get('path')
	url = kwargs.get('url')
	client = kwargs.get('client')
	oauth_key = kwargs.get('oauth_key', '')
	fingerprint = kwargs.get('fingerprint')
	query_params = kwargs.get('query_params')
	headers = generate_headers(
		client=client,
		oauth_key=oauth_key,
		fingerprint=fingerprint,
		ip_address=kwargs.get('ip_address')
	)
	if path:
		url = client.get_base_path() + path
		response = requests.get(url, headers=headers, params=query_params)
	else:
		response = requests.get(url, headers=headers, params=query_params)
	return determine_response(response=response)

def delete(**kwargs):
	"""Summary
	
	Args:
	    **kwargs: Description
	
	Returns:
	    TYPE: Description
	"""
	path = kwargs.get('path')
	url = kwargs.get('url')
	client = kwargs.get('client')
	oauth_key = kwargs.get('oauth_key', '')
	fingerprint = kwargs.get('fingerprint')
	headers = generate_headers(
		client=client,
		oauth_key=oauth_key,
		fingerprint=fingerprint,
		ip_address=kwargs.get('ip_address')
	)
	if path:
		url = client.get_base_path() + path
		response = requests.delete(url, headers=headers)
	else:
		response = requests.delete(url, headers=headers)
	return determine_response(response=response)

def patch(**kwargs):
	"""Summary
	
	Args:
	    **kwargs: Description
	
	Returns:
	    TYPE: Description
	"""
	path = kwargs.get('path')
	url = kwargs.get('url')
	client = kwargs.get('client')
	oauth_key = kwargs.get('oauth_key', '')
	fingerprint = kwargs.get('fingerprint')
	payload = kwargs.get('payload')
	headers = generate_headers(
		client=client,
		oauth_key=oauth_key,
		fingerprint=fingerprint,
		ip_address=kwargs.get('ip_address')
	)
	if path:
		url = client.get_base_path() + path
		response = requests.patch(url, headers=headers, data=json.dumps(payload))
	else:
		response = requests.patch(url, headers=headers, data=json.dumps(payload))
	return determine_response(response=response)

def post(**kwargs):
	"""Summary
	
	Args:
	    **kwargs: Description
	
	Returns:
	    TYPE: Description
	"""
	path = kwargs.get('path')
	url = kwargs.get('url')
	client = kwargs.get('client')
	oauth_key = kwargs.get('oauth_key', '')
	fingerprint = kwargs.get('fingerprint')
	payload = kwargs.get('payload')
	headers = generate_headers(
		client=client,
		fingerprint=fingerprint,
		oauth_key=oauth_key,
		ip_address=kwargs.get('ip_address')
	)
	if path:
		url = client.get_base_path() + path
		response = requests.post(url, headers=headers, data=json.dumps(payload))
	else:
		response = requests.post(url, headers=headers, data=json.dumps(payload))
	return determine_response(response=response)

def generate_headers(**kwargs):
	"""Summary
	
	Args:
	    **kwargs: Description
	
	Returns:
	    TYPE: Description
	"""
	oauth_key = kwargs.get('oauth_key', '')
	client = kwargs.get('client')
	fingerprint = kwargs.get('fingerprint')
	headers = {
		'X-SP-GATEWAY':client.client_id + '|' + client.client_secret,
		'X-SP-USER':oauth_key + '|' + fingerprint,
		'X-SP-USER-IP': kwargs.get('ip_address'),
		'X-SP-LANG': 'en',
		'Content-Type':'application/json'
	}
	return headers

def determine_response(**kwargs):
	"""Summary
	
	Args:
	    **kwargs: Description
	
	Returns:
	    TYPE: Description
	"""
	response = kwargs.get('response')
	if response.status_code == 200:
		return response.json()
	elif response.status_code == 202:
		return response.json()
	elif response.status_code == 400:
		raise APIError(response.json()['error']['en'])
	elif response.status_code == 401:
		raise APIError(response.json()['error']['en'])
	elif response.status_code == 404:
		raise APIError(response.json()['error']['en'])
	elif response.status_code == 409:
		raise APIError(response.json()['error']['en'])
	elif response.status_code == 500:
		raise APIError(response.json()['error']['en'])
	else:
		raise APIError({
			'http_code':response.status_code,
			'error_code':None,
			'error':{
				'en':'Could not connect to the server.'
			}
		})

class APIError(Exception):
	"""Summary"""
	pass
