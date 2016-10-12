import unittest
from Helpers import *
from synapse_pay import HTTPClient, Users, Nodes, Transactions
from synapse_pay.Node import Node


class TransactionsTestCases(unittest.TestCase):

    def setUp(self):
        client = HTTPClient(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            is_production=False
        )
        user = Users.get(
            _id=VERIFIED_USER_ID,
            client=client,
            fingerprint=FINGERPRINT,
            ip_address=IP_ADDRESS
        )
        nodes = Nodes.get(user=user, client=client)
        self.node = Node(json=nodes['nodes'][0], user=user)

    def create_transaction(self):
        trans_payload = {
            "to": {
                "type": "SYNAPSE-US",
                "id": TO_NODE_ID
            },
            "amount": {
                "amount": 2.10,
                "currency": "USD"
            },
            "extra": {
                "supp_id": "1283764wqwsdd34wd13212",
                "note": "Deposit to bank account",
                "webhook": "http://requestb.in/q94kxtq9",
                "process_on": 1,
                "ip": "192.168.0.1",
                "other": {
                    "attachments": []
                }
            },
            "fees": [{
                "fee": 1.00,
                "note": "Facilitator Fee",
                "to": {
                    "id": "55d9287486c27365fe3776fb"
                }
            }]
        }
        transaction = Transactions.create(node=self.node, payload=trans_payload)
        return transaction

    def test_create_success(self):
        transaction = self.create_transaction()
        self.assertTrue(transaction.json != None)

    def test_get_success(self):
        trans_id = self.create_transaction().json['_id']
        transaction = Transactions.get(node=self.node, _id=trans_id)
        self.assertTrue(transaction.json != None)


if __name__ == '__main__':
    unittest.main()
