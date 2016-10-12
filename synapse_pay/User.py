"""Summary"""
from synapse_pay import HTTPClient


class User(object):
    """Abstraction of the /users endpoint."""

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

    def get(self, **kwargs):
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
            path = self.BASE_PATH + '/' + _id
            response = HTTPClient.get(
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
            response = HTTPClient.get(
                client=client,
                path=self.BASE_PATH,
                fingerprint='',
                ip_address='',
                query_params=query_params
            )
            return response

    def post(self, **kwargs):
        """Summary

        Args:
            **kwargs: Description

        Returns:
            TYPE: Description
        """
        client = kwargs.get('client')
        fingerprint = kwargs.get('fingerprint')
        ip_address = kwargs.get('ip_address')
        response = HTTPClient.post(
            client=client,
            fingerprint=fingerprint,
            payload=kwargs.get('payload'),
            ip_address=ip_address,
            path=self.BASE_PATH
        )
        return User(
            client=client,
            json=response,
            fingerprint=fingerprint,
            ip_address=ip_address
        )

    def get_oauth_key(self):
        """Summary

        Returns:
            TYPE: Description
        """
        payload = {
            'refresh_token': self.json['refresh_token']
        }
        path = 'api/3/oauth/{0}'.format(self.json['_id'])
        response = HTTPClient.post(
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
        response = HTTPClient.patch(
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
        DEPRECATED
        Args:
            **kwargs: Description

        Returns:
            TYPE: Description
        """
        response = HTTPClient.patch(
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
        DEPRECATED
        Args:
            **kwargs: Description

        Returns:
            TYPE: Description
        """
        response = HTTPClient.patch(
            client=self.client,
            oauth_key=self.oauth_key,
            url=self.json['_links']['self']['href'],
            fingerprint=self.fingerprint,
            payload=kwargs.get('payload'),
            ip_address=self.ip_address
        )
        self.json = response
        return response
