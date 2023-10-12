#START CALLS EVENT MESSAGE CONTRACT
import json
from web3 import Web3
import pandas as pd
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

account_1 = "0xED51d93b9fF5E82620cdA25Cb13ED32749867a0B"
account_2 = "0x407fEfF75B7DC8B3146A385a7D783B4a791553B6"
private_key = "05754b5cef7d732252b8b411be96f38c870a25ba6f2729a534b9898b7e351e7a"

abi = json.loads('[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"id","type":"bytes32"},{"indexed":false,"internalType":"address","name":"addr","type":"address"},{"indexed":false,"internalType":"bytes32","name":"balance","type":"bytes32"},{"indexed":false,"internalType":"bytes32","name":"trust_value","type":"bytes32"}],"name":"registerevent","type":"event"},{"inputs":[{"internalType":"bytes32","name":"id","type":"bytes32"},{"internalType":"address","name":"initiator","type":"address"},{"internalType":"bytes32","name":"balance","type":"bytes32"},{"internalType":"bytes32","name":"trust_value","type":"bytes32"}],"name":"Initiator","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"initiator","type":"address"}],"name":"viewevent","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"address","name":"","type":"address"},{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}]')
bytecode = "608060405260043610610028575f3560e01c806317f1ce911461002c578063529efbca14610048575b5f80fd5b610046600480360381019061004191906104fa565b610087565b005b348015610053575f80fd5b5061006e6004803603810190610069919061055e565b610334565b60405161007e94939291906105a7565b60405180910390f35b8360015f8573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f01819055508260015f8573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f206001015f6101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508160015f8573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f20600201819055508060015f8573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f20600301819055507fe3613e4536bde6a5a273b0ad1f73e2d407468b885d1ee085121d355cca88ede660015f8573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f015460015f8673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f206001015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1660015f8773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f206002015460015f8873ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f206003015460405161032694939291906105a7565b60405180910390a150505050565b5f805f8060015f8673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f015460015f8773ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f206001015f9054906101000a900473ffffffffffffffffffffffffffffffffffffffff1660015f8873ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f206002015460015f8973ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f206003015493509350935093509193509193565b5f80fd5b5f819050919050565b61047f8161046d565b8114610489575f80fd5b50565b5f8135905061049a81610476565b92915050565b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f6104c9826104a0565b9050919050565b6104d9816104bf565b81146104e3575f80fd5b50565b5f813590506104f4816104d0565b92915050565b5f805f806080858703121561051257610511610469565b5b5f61051f8782880161048c565b9450506020610530878288016104e6565b93505060406105418782880161048c565b92505060606105528782880161048c565b91505092959194509250565b5f6020828403121561057357610572610469565b5b5f610580848285016104e6565b91505092915050565b6105928161046d565b82525050565b6105a1816104bf565b82525050565b5f6080820190506105ba5f830187610589565b6105c76020830186610598565b6105d46040830185610589565b6105e16060830184610589565b9594505050505056fea264697066735822122061d9d5201a62de39b0d395fcc00057d93394e3a4e2935c16498ab1d74db13e4764736f6c63430008150033"

#web3.eth.defaultAccount = web3.eth.accounts[0]
message = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = message.constructor().transact()
tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
deployed_address = tx_receipt["contractAddress"]

#Reference the deployed contract:
message = web3.eth.contract(address = deployed_address, abi=abi)

addresses_df = pd.read_csv(
    'test.txt',
    header=None, names=['id', 'address', 'balance', 'trust_value']
)

#manually build and sign a transaction:
nonce_count = web3.eth.get_transaction_count(account_2)
for row in addresses_df.itertuples():
	nonce_cnt = int(nonce_count)
	unsent_tx = message.functions.Initiator(row.id, row.address, row.balance, row.trust_value).build_transaction({
		"from": "account_2",
		"to": row.address,
		"nonce": nonce_cnt,
		'gas': 100000,
        'gasPrice': 1000000000,
})
signed_tx = web3.eth.account.sign_transaction(unsent_tx, private_key=private_key)
print(signed_tx)
print('event information: {}'.format(message.functions.viewevent().call()))

#END CALLS EVENT MESSAGE CONTRACT