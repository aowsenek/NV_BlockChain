import json
import time
import random
import pprint
import hashlib
import mygeotab
import calendar
import contract_abi
import Crypto.PublicKey.RSA as RSA
from web3 import Web3, HTTPProvider
from SENSITIVE_DATA import *
w3 = Web3(HTTPProvider('https://ropsten.infura.io/v3/5af6561b0144467d873a662587677aae'))
contract = w3.eth.contract(address = Web3.toChecksumAddress(CONTRACT_ADDRESS), abi = contract_abi.abi)
LinesOfData = 10
class VehicleBlockchain():
    def __init__(self, signature):
        self.parentHash = signature
        self.binDifficulty = bin(int("dab",16))
        self.strDifficulty = "dab"
        self.nonce = 0#random()*100
        self.blockChain = {}
        self.data = None

    def incrementDifficulty(self): #doesn't work yet
        hexArr = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
        if(self.difficulty[-1] == "f"):
            self.difficulty = self.difficulty+1
        else:
            self.difficulty[-1] = bin(int(hexArr[hexArr.find(self.difficulty[-1])+1],16))

    def binHashCriteria(self, hash):
        binhash = bin(int(hash,16))[:len(self.binDifficulty)]
        if(binhash == self.binDifficulty):
            return True
        return False

    def hashCriteria(self, hash):
        hash = hash[:len(self.strDifficulty)]
        if(hash == self.strDifficulty):
            return True
        return False

    def MakeBlock(self, data): #sign with key
        block = [self.parentHash, data, self.nonce]
        hash = hashlib.sha256(';'.join(map(str,block)).encode('utf-8')).hexdigest()
        while(not self.hashCriteria(hash)):
            self.nonce += 1
            block = [self.parentHash, data, self.nonce]
            hash = hashlib.sha256(';'.join(map(str,block)).encode('utf-8')).hexdigest()
            if(self.nonce%100000 == 0): print(self.nonce)
        self.blockChain[hash] = block
        self.parentHash = hash
        print(publishData(hash,int(calendar.timegm(time.gmtime())),self.nonce))
        #print("A New Block Touches the Beacon:", block, "Hash:", hash)

    def startChain(self, numBlocks):
        for i in range(numBlocks):
            data = "Starter Block"
            self.MakeBlock(data)

    def print(self):
        pprint.pprint(self.blockChain)

    def printLastBlock(self):
        print(list(self.blockChain.keys())[-1],":",self.blockChain[list(self.blockChain.keys())[-1]])

def getGeoTabData():
    api = mygeotab.API(username=GEOTAB_USERNAME, password=GEOTAB_PASSWORD, database='NV_Dan')
    api.authenticate()

    data = api.getfeed()
    json_string = json.dumps(data, indent=4, sort_keys=True, default=str)
    return json_string

def publishData(hash, epoch, nonce):
    num = w3.eth.getTransactionCount(WALLET_ADDRESS)
    txn_dict = contract.functions.addHash(hash,epoch,nonce).buildTransaction({
        'chainId': 3,
        'gas': 1400000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': num,
    })
    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=WALLET_PRIVATE_KEY)
    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    txn_receipt = w3.eth.getTransactionReceipt(result)

    count = 0
    while(txn_receipt is None and (count < 30)):
        time.sleep(10)
        txn_receipt = w3.eth.getTransactionReceipt(result)
        print(txn_receipt)
    if(txn_receipt is None): 
        print("Transaction Failed; Timeout.")
        return False
    prcs_receipt = contract.events.NewBlock().processReceipt(txn_receipt)
    print(prcs_receipt)
    return True

def eventLoop():
    pubkey = open("nv_keys.pub").read()
    blockchain = VehicleBlockchain(pubkey)
    blockchain.startChain(5)
    mockdata = open("MOCK_DATA.json","r")
    api = mygeotab.API(username=GEOTAB_USERNAME, password=GEOTAB_PASSWORD, database='NV_Dan')
    api.authenticate()
    
    for i in range(5):#while(True):
        data = []
        for i in range(LinesOfData):
            data.append(mockdata.readline())
        blockchain.MakeBlock(data)
        blockchain.printLastBlock()
    

if(__name__ == "__main__"):
    eventLoop()



