"""Miscellaneous functions that could be useful when interacting with the SynapsePay API"""
import base64
import mimetypes
import requests
import hashlib
import hmac

def file_to_base64(**kwargs):
	"""
	Converts a file path into a correctly padded base64 representation
	for the SynapsePay API.  Mimetype padding is done by file 
	extension not by content(for now).
	
	Args:
	    **kwargs: file_path
	
	Returns:
	    str: Base64 representation of the file.
	"""
	file_path = kwargs.get('file_path')
	with open(file_path, 'wb') as file_object:
		encoded_string = base64.b64encode(file_object.read())
		mime_type = mimetypes.guess_type(file_object.name)[0]
		mime_padding = 'data:' + mime_type + ';base64,'
		base64_string = mime_padding + encoded_string
		return base64_string

def url_to_base64(**kwargs):
	"""
	Converts a url into a correctly padded base64 representation
	for the SynapsePay API.  Mimetype padding is done by file 
	extension not by content(for now).
	
	Args:
	    **kwargs: url
	
	Returns:
	    str: Base64 representation of the file.
	"""
	url = kwargs.get('url')
	response = requests.get(url)
	mime_type = mimetypes.guess_type(url)[0]
	uri = ("data:" + mime_type + ";" +"base64," + base64.b64encode(response.content))
	return uri

def stream_to_base64(**kwargs):
	"""
	Converts a url into a correctly padded base64 representation
	for the SynapsePay API.  Mimetype padding is done by file 
	extension not by content(for now).
	
	Args:
	    **kwargs: url
	
	Returns:
	    str: Base64 representation of the file.
	"""
	file_object = kwargs.get('stream')
	encoded_string = base64.b64encode(file_object.read())
	mime_type = mimetypes.guess_type(file_object.name)[0]
	mime_padding = 'data:' + mime_type + ';base64,'
	base64_string = mime_padding + encoded_string
	return base64_string

def validate_hmac(**kwargs):
	"""
	Validates a given hmac with your client_secret, client_id, and object id.
	
	Args:
	    **kwargs:	client_id - your SynapsePay client_id
	    			client_secret - your SynapsePay client_secret
	    			object_id - the object id received from SynapsePay
	    			hmac - the hmac received along with the object_id
	
	Returns:
	    bool: True if the hmac is valid, false if it isn't.
	"""
	given_hmac = kwargs.get('hmac')
	client_secret = kwargs.get('client_secret')
	client_id = kwargs.get('client_id')
	object_id = kwargs.get('object_id')
	raw = '{0}+{1}'.format(object_id, client_id)
	sha1 = hashlib.new('sha1')
	hashed = hmac.new(client_secret, raw, sha1)
	return given_hmac == hashed.hexdigest()
