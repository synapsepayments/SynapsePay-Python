"""Summary"""
import requests
import json
import logging
from .APIError import APIError


class HTTPClient(object):
    def __init__(self, **kwargs):
        """Constructor

        Args:
            **kwargs:   client_id - your SynapsePay client_id
                        client_secret - your SynapsePay client_secret
                        is_production - boolean to ping either sandbox or is_production
                        log_requests - boolean on whether to log every http request
        """
        self.header_config = {
            'client_id': kwargs['client_id'],
            'client_secret': kwargs['client_secret'],
            'fingerprint': kwargs['fingerprint'],
            'ip_address': kwargs['ip_address']
        }
        self.is_production = kwargs.get('is_production', False)
        self.base_url = self.get_base_url()
        self.log_requests = kwargs.get('log_requests', False)
        if self.log_requests:
            self.start_logging()

    def start_logging(self):
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

    def generate_headers(self):
        """Summary

        Args:
            **kwargs: Description

        Returns:
            TYPE: Description
        """
        client_id = self.header_config['client_id']
        client_secret = self.header_config['client_secret']
        fingerprint = self.header_config['fingerprint']
        ip_address = self.header_config['ip_address']
        oauth_key = self.header_config.get('oauth_key')

        headers = {
            'Content-Type': 'application/json',
            'X-SP-LANG': 'en',
            'X-SP-GATEWAY': '|'.join([client_id, client_secret]),
            'X-SP-USER': '|'.join([oauth_key, fingerprint]),
            'X-SP-USER-IP': ip_address
        }
        return headers

    def update_headers(self, **kwargs):
        """Update header dict with any new key values.
        """
        for key in self.header_config:
            if kwargs.get(key):
                self.header_config[key] = kwargs[key]

    def get_base_url(self):
        """Returns the API base url for sandbox or production env.

        Returns:
            TYPE: Description
        """
        if self.is_production:
            return 'https://synapsepay.com/'
        else:
            return 'https://sandbox.synapsepay.com/'

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
                'http_code': response.status_code,
                'error_code': None,
                'error': {
                    'en': 'Could not connect to the server.'
                }
            })
