import time
import random
import pickle
import hashlib
import calendar
from Crypto.Hash import SHA256
from threading import Thread
import numpy as np

#globals
Difficulty = "0000"
BlockLength = 10 #Time between block data 
BlockTime = 10 #Time between blocks
ketchupChain = []#Time
anchorBlockChain = []
parentHashGood = 00000000000000000000000000000000
parentHashEvil = 00000000000000000000000000000000
goodPrinted = False
evilPrinted = False
Data = {} #data for graphs
timeToGeneration = 5
avgGenerationTime = 2
timeToEclipse = {25:None,50:None,75:None,100:None}
pickleFile = open('100Blocks.pkl', 'rb')

def resetGlobals():
    global anchorBlockChain, ketchupChain, parentHashGood, parentHashEvil, goodPrinted, evilPrinted
    anchorBlockChain = []#Time
    ketchupChain = []#Time
    parentHashGood = 00000000000000000000000000000000
    parentHashEvil = 00000000000000000000000000000000
    goodPrinted = False
    evilPrinted = False
    timeToEclipse = {25:None,50:None,75:None,100:None}

#Do the blockchain
def AutoAdjustDifficulty(): #In seconds
    global Difficulty, anchorBlockChain, ketchupChain, timeToGeneration, avgGenerationTime
    #hexArr = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
    try:
        avgGenerationTime = (((anchorBlockChain[-1] - anchorBlockChain[0]))+(ketchupChain[-1]-ketchupChain[0]))/(len(anchorBlockChain)+len(ketchupChain))
       # print("ADJUST:",avgGenerationTime)
       # if(avgGenerationTime < (timeToGeneration-5)):
       #     Difficulty += "0"
       # elif(avgGenerationTime > (timeToGeneration+5)):
       #      Difficulty = Difficulty[:-1]
      #  print(Difficulty)
    except:
        return
        
def hashCriteria(hash):
    hash = hash[:len(Difficulty)]
    if(hash == Difficulty):
        return True
    return False

def MakeBlock(parentHash, data): 
    nonce = int(getRandData())
    block = [parentHash, data, nonce]
    hash = hashlib.sha256(';'.join(map(str,block)).encode('utf-8')).hexdigest()
    while(not hashCriteria(hash)):
        if(len(ketchupChain) >= len(anchorBlockChain)+1):
            return parentHash, None
        nonce += 1
        block = [parentHash, data, nonce]
        hash = hashlib.sha256(';'.join(map(str,block)).encode('utf-8')).hexdigest()
        AutoAdjustDifficulty()
    epoch = time.time() #int(calendar.timegm(time.gmtime())) #Time in seconds since epoch
    return hash, epoch
        
def getRandData():
    time.sleep(1)
    return random.random()*10000000000 + random.random()*100000000

#Run the stuff
def startThreadEvil():
    global parentHashEvil, ketchupChain, anchorBlockChain, evilPrinted, timeToEclipse
    #print("Starting Evil")
    tim = 0
    while(len(ketchupChain) <= len(anchorBlockChain)+1):
        data = getRandData()
        parentHashEvil, tim = MakeBlock(parentHashEvil, data)
        if((len(ketchupChain)+1)%25 == 0): isAnchor = True
        else: isAnchor = False
        if(tim != None):
            ketchupChain.append((parentHashGood, data, tim, isAnchor))
        else: return
        #if(len(ketchupChain)%5==0): 
        AutoAdjustDifficulty()
    if(not evilPrinted):
        evilPrinted = True
        #print("Evil:",ketchupChain)

def startThreadGood():
    global parentHashGood, anchorBlockChain, ketchupChain, goodPrinted, timeToEclipse
    #print("Starting Good")
    tim = 0
    isAnchor = False
    while(len(ketchupChain) <= len(anchorBlockChain)+1):
        data = getRandData()
        if((len(anchorBlockChain)+1)%25 == 0): isAnchor = True
        else: isAnchor = False
        parentHashGood, tim = MakeBlock(parentHashGood, data)
        if(tim != None):
            anchorBlockChain.append((parentHashGood, data, tim, isAnchor))
        else: return
        #if(len(anchorBlockChain)%5==0): 
        AutoAdjustDifficulty()
    if(not goodPrinted):
        goodPrinted = True
        #print("Good:",anchorBlockChain)
    

def eventLoop(numGood=7, numThreads = 10): 
    global ketchupChain, anchorBlockChain, timeToEclipse
    thread = [0]*numThreads
    for i in range(numGood):
        thread[i] = Thread(target = startThreadGood)
        thread[i].start()
    time.sleep(1)
    for i in range(numGood,numThreads):
        thread[i] = Thread(target = startThreadEvil)
        thread[i].start()
    for i in thread:
        i.join()
    
    #print(ketchupChain)
    relevantTuples = list(filter(lambda t: t[3]==True, ketchupChain))
    #print(relevantTuples)
    for i in range(len(relevantTuples)):
        timeToEclipse[(i+1)*25] = relevantTuples[i][2]-ketchupChain[0][2]
    #print(timeToEclipse)
    return timeToEclipse


def GenerateChain(num=100):
    global anchorBlockChain, parentHashGood
    isAnchor = False
    for i in range(1,num+1):
        if(i%25 == 0): isAnchor = True
        else: isAnchor = False
        data = getRandData()
        parentHashGood, tim = MakeBlock(parentHashGood, data)
        anchorBlockChain.append((parentHashGood, data, tim, isAnchor))

    pickle.dump(anchorBlockChain, pickleFile)
    print(anchorBlockChain)
    pickleFile.close()

#GenerateChain()

anchorBlockChain = pickle.load(pickleFile)
pickleFile.close()

runs = 10
NumGThreads = 1
DifThreads = {}
def getStatData():
    global DifThreads, NumGThreads, Difficulty, runs
    for j in range(runs):#numDifficulties
        try:
            tte = eventLoop(numGood = NumGThreads)
        except:
            pass
        resetGlobals()
        DifThreads[j] = tte


getStatData()
print(DifThreads)

