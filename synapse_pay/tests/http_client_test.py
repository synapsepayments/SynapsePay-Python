import unittest
from synapse_pay.HTTPClient import HTTPClient
from .TestHelpers import *


class HttpClientTestCases(unittest.TestCase):
    def setUp(self):
        self.http_client = HTTPClient(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            fingerprint=FINGERPRINT,
            ip_address=IP_ADDRESS,
            is_production=False,
            log_requests=True
        )

    def test_base_url_depends_on_production_flag(self):
        sandbox = 'https://sandbox.synapsepay.com/'
        production = 'https://synapsepay.com/'
        self.assertEqual(sandbox, self.http_client.base_url)

        prod_http_client = HTTPClient(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            fingerprint=FINGERPRINT,
            ip_address=IP_ADDRESS,
            is_production=True,
            log_requests=True
        )
        self.assertEqual(production, prod_http_client.base_url)

    def test_generate_headers_builds_a_dict_init_kwargs(self):
        http_client = self.http_client
        headers = http_client.generate_headers()
        gateway = CLIENT_ID + '|' + CLIENT_SECRET
        user = '|' + FINGERPRINT
        self.assertEqual(gateway, headers['X-SP-GATEWAY'])
        self.assertEqual(user, headers['X-SP-USER'])
        self.assertEqual(IP_ADDRESS, headers['X-SP-USER-IP'])

    def test_update_headers_updates_the_specified_kwargs(self):
        http_client = self.http_client
        new_oauth_key = 'oauth_key'
        http_client.update_headers(oauth_key=new_oauth_key)
        headers = http_client.generate_headers()
        gateway = CLIENT_ID + '|' + CLIENT_SECRET
        user = new_oauth_key + '|' + FINGERPRINT
        self.assertEqual(gateway, headers['X-SP-GATEWAY'])
        self.assertEqual(user, headers['X-SP-USER'])
        self.assertEqual(IP_ADDRESS, headers['X-SP-USER-IP'])
