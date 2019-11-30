import pdb, base64
import fire
import json
import time
import random
import pprint
import hashlib
import calendar
import contract_abi
#from web3 import Web3, HTTPProvider
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA as rsa
from Crypto.Signature import PKCS1_v1_5
#from SENSITIVE_DATA import *
#w3 = Web3(HTTPProvider('https://ropsten.infura.io/v3/5af6561b0144467d873a662587677aae'))
#contract = w3.eth.contract(address = Web3.toChecksumAddress(CONTRACT_ADDRESS), abi = contract_abi.abi)
BlockTime = 10
class VehicleBlockchain():
    def __init__(self, pubkey, privkey):
        self.parentHash = pubkey
        self.privkey = PKCS1_v1_5.new(privkey)
        self.binDifficulty = bin(int("000",16))
        self.strDifficulty = "000"
        self.nonce = 0#random()*100
        self.blocknum = 0
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
        epoch = int(calendar.timegm(time.gmtime()))
        digest = SHA256.new()
        digest.update(hash.encode('utf-8'))
#        pdb.set_trace()

        signature = str(base64.b64encode(self.privkey.sign(digest)),'utf-8')

        self.blockChain[self.blocknum] = {'block':block,'hash':hash,'sig':signature,'time':epoch}
        #print(publishData(hash,epoch,self.nonce))
        with open("blockChain.json","w") as fileb:
            json.dump(self.blockChain, fileb)
        self.parentHash = hash
        self.blocknum += 1

        print("Hash:", hash)

    def startChain(self, numBlocks):
        for i in range(numBlocks):
            data = "Starter Block"
            self.MakeBlock(data)

    def pirint(self):
        pprint.pprint(self.blockChain)

    def pirintLastBlock(self):
        print(list(self.blockChain.keys())[-1],":",self.blockChain[list(self.blockChain.keys())[-1]])

def getRandData():
    time.sleep(BlockTime)
    data = random.random()*10000000000 + random.random()*100000000

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
    #print(prcs_receipt)
    return True

def getRSAKeys(gen):
    if(gen == "generate"):
        privkey = rsa.generate(2048)
        pubkey = privkey.publickey()
        with open ("nv_keys", "w") as prv_file:
            print("{}".format(privkey.exportKey(format='PEM')), file=prv_file)

        with open ("nv_keys.pub", "w") as pub_file:
            print("{}".format(pubkey.exportKey(format='PEM')), file=pub_file)
            pubkey = str(pubkey.exportKey(format='PEM'),'utf-8')
    else:
        with open('nv_keys', mode = 'rb') as privatefile:
            keydata = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(keydata)
        with open('nv_keys.pub', mode = 'rb') as privatefile:
            keydata = privatefile.read()
        pubkey = rsa.PrivateKey.load_pkcs1(keydata)
    return pubkey,privkey

def eventLoop():
    pubkey,privkey = getRSAKeys("generate")
    blockchain = VehicleBlockchain(pubkey,privkey)
    blockchain.startChain(5)
    mockdata = getRandData()
    
    while(True):
        blockchain.MakeBlock(mockdata)
        #blockchain.printLastBlock()

def main(Bloctime = 10):
    global BlockTime
    BlockTime = Bloctime
    eventLoop()

if(__name__ == "__main__"):
    fire.Fire(main)



