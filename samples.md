
## Initialization

```python


# Imports

from synapse_pay import *


# Instantiate

client = Clients(
	client_id='CLIENT_ID',
	client_secret='CLIENT_SECRET',
	is_production=False
)

```

## User API Calls

```python


# Get All Users

users = Users.get(client=client)

# users is a JSON object


#Create a User

create_payload = {
	"logins": [
		{
			"email": "pythonTest@synapsepay.com",
			"password": "test1234",
			"read_only":False
		}
	],
	"phone_numbers": [
		"901.111.1111"
	],
	"legal_names": [
		"PYTHON TEST USER"
	],
	"extra": {
		"note": "Interesting user",
		"supp_id": "122eddfgbeafrfvbbb",
		"is_business": False
	}
}

user = Users.create(
	client=client,
	payload=create_payload,
	fingerprint='FINGERPRINT',
	ip_address='IP_ADDRESS'
)


# Get User

user = Users.get(
	client=client,
	_id=USER_ID,
	fingerprint='FINGERPRINT',
	ip_address='IP_ADDRESS'
)

# user is an instance of the User object


# Update User

update_payload = {
	"refresh_token": "REFRESH_TOKEN",
	"update":{
		"login": {
			"email": "test2python@email.com",
			"password": "test1234",
			"read_only": True
		},
		"phone_number": "9019411111",
		"legal_name": "Some new name"
	}
}

update_response = user.update(payload=update_payload)

# update_response is a dict but the user object is also updated


# Add Document

ssn_payload = {
		"doc":{
		"birth_day":4,
		"birth_month":2,
		"birth_year":1940,
		"name_first":"John",
		"name_last":"doe",
		"address_street1":"1 Infinite Loop",
		"address_postal_code":"95014",
		"address_country_code":"US",
		"document_value":"3333",
		"document_type":"SSN"
	}
}

ssn_response = user.add_doc(payload=ssn_payload)

# ssn_response is a dict but the user object is updated if no kba needed


# Answer KBA Questions

kba_payload = {
	"doc":{
		"question_set_id":"557520ad343463000300005a",
		"answers":[
			{ "question_id": 1, "answer_id": 1 },
			{ "question_id": 2, "answer_id": 1 },
			{ "question_id": 3, "answer_id": 1 },
			{ "question_id": 4, "answer_id": 1 },
			{ "question_id": 5, "answer_id": 1 }
		]
	}
}

kba_response = user.answer_kba(payload=kba_payload)

# kba_response is a dict but the user object is also updated


# Attach a File

base64 = Helpers.url_to_base64(url='url_of_file')

file_payload = {
	'doc':{
		'attachment': base_64
	}
}

file_response = user.update(payload=file_payload)

# file_response is a dict but the user object is also updated

```

## User Object

```python


# Imports

from synapse_pay import User


# Instantiation

user = User(
	client=client, # a client Object
	json=response, # SynapsePay JSON user object
	fingerprint=fingerprint, # their fingerprint
	ip_address=ip_address # ip address of the user
)

# A user object uses the json provided to automatically authenticate the user through # the refresh token provided in the json.  You do not need to refresh this object.


```

## Node API Calls

```python


# Imports

from synapse_pay import Nodes, Node


# Get All Nodes

nodes = Nodes.get(user=user)

# nodes is a JSON object


# Add SYNAPSE-US Node

synapse_node_payload = {
	"type":"SYNAPSE-US",
	"info":{
		"nickname":"My Synapse Wallet"
	},
	"extra":{
		"supp_id":"123sa"
	}
}

node = Nodes.create(payload=synapse_node_payload)

# node is an instance of the Node class


# Add ACH-US node through account login

login_payload = {
	"type":"ACH-US",
	"info":{
		"bank_id":"synapse_good",
		"bank_pw":"test1234",
		"bank_name":"fake"
	}
}

login_response = Nodes.create(user=user, payload=login_payload)

# login_response is a JSON response if mfa otherwise an instance of the Node class


# Verify ACH-US Node via MFA

mfa_payload = {
	"access_token":ACCESS_TOKEN_IN_LOGIN_RESPONSE,
	"mfa_answer":"test_answer"
}

node = Nodes.create(user=user, payload=mfa_payload)

# node is a JSON response if mfa otherwise an instance of the Node class


# Add ACH-US Node through Account and Routing Number Details

acct_rout_payload = {
	"type":"ACH-US",
	"info":{
		"nickname":"Python Library Savings Account",
		"name_on_account":"Python Library",
		"account_num":"72347235423",
		"routing_num":"051000017",
		"type":"PERSONAL",
		"class":"CHECKING"
	},
	"extra":{
		"supp_id":"123sa"
	}
}

node = Nodes.create(user=user, payload=acct_rout_payload)

# node is an instance of the Node class


# Verify ACH-US Node via Micro-Deposits

micro_payload = {
	"micro":[0.1,0.1]
}

micro_response = node.update(payload=micro_payload)

# micro_response is a JSON object but the node object has also been updated


# Delete a Node

success = node.delete()

# success is a boolean


```

## Transaction API Calls

```python

# Get All Transactions

transactions_response = Transactions.get(node=node)

# transactions_response is a dict


# Create a Transaction

trans_payload = {
	"to":{
		"type":"SYNAPSE-US",
		"id":"560adb4e86c27331bb5ac86e"
	},
	"amount":{
		"amount":1.10,
		"currency":"USD"
	},
	"extra":{
		"supp_id":"1283764wqwsdd34wd13212",
		"note":"Deposit to bank account",
		"webhook":"http://requestb.in/q94kxtq9",
		"process_on":1,
		"ip":"192.168.0.1"
	},
	"fees":[{
		"fee":1.00,
		"note":"Facilitator Fee",
		"to":{
			"id":"55d9287486c27365fe3776fb"
		}
	}]
}

transaction = Transactions.create(node=node, payload=trans_payload)

# transaction is an instance of the Transaction class


# Get a Transaction

transaction = Transactions.get(node=node, _id=TRANS_ID)

# transaction is an instance of the Transaction class


# Update Transaction

update_payload = {
	"comment": "hi"
}

update_response = transaction.update(payload=update_payload)

# update_response is a dict but the transaction object has also been updated


# Delete Transaction

success = transaction.delete()

# success is a boolean

```

## Miscellaneous

```python

# Base 64 Converters

base64_padded = Helpers.file_to_base64(path=path)

base64_padded = Helpers.url_to_base64(url=url)

base64_padded = Helpers.stream_to_base64(stream=stream)

# base64_padded is a string


# HMAC Validation

valid = Helpers.validate_hmac(
	hmac='HMAC',
	client_secret='CLIENT_SECRET',
	client_id='CLIENT_ID',
	object_id='OBJECT_ID'
)

# valid is a boolean

```
