abi = """
[
	{
		"constant": false,
		"inputs": [
			{
				"name": "hash",
				"type": "string"
			},
			{
				"name": "epoch",
				"type": "uint256"
			},
			{
				"name": "nonce",
				"type": "uint256"
			}
		],
		"name": "addHash",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"name": "hash",
				"type": "string"
			},
			{
				"indexed": false,
				"name": "epoch",
				"type": "uint256"
			},
			{
				"indexed": false,
				"name": "nonce",
				"type": "uint256"
			}
		],
		"name": "NewBlock",
		"type": "event"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "Block_Data",
		"outputs": [
			{
				"name": "hash",
				"type": "string"
			},
			{
				"name": "epoch",
				"type": "uint256"
			},
			{
				"name": "nonce",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "blockNumber",
				"type": "uint256"
			}
		],
		"name": "getHash",
		"outputs": [
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]"""

