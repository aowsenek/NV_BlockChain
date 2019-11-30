import time
import random
import hashlib
import calendar
from Crypto.Hash import SHA256
from threading import Thread
import numpy as np

#globals
Difficulty = "0"
BlockLength = 10 #Time between block data 
BlockTime = 10 #Time between blocks
timeChainGood = []#Time
timeChainEvil = []#Time
parentHashGood = 00000000000000000000000000000000
parentHashEvil = 00000000000000000000000000000000
goodPrinted = False
evilPrinted = False
Data = {} #data for graphs
timeToGeneration = 5
avgGenerationTime = 2

def resetGlobals():
    global timeChainGood, timeChainEvil, parentHashGood, parentHashEvil, goodPrinted, evilPrinted
    timeChainGood = []#Time
    timeChainEvil = []#Time
    parentHashGood = 00000000000000000000000000000000
    parentHashEvil = 00000000000000000000000000000000
    goodPrinted = False
    evilPrinted = False

#Do the blockchain
def AutoAdjustDifficulty(): #In seconds
    global Difficulty, timeChainGood, timeChainEvil, timeToGeneration, avgGenerationTime
    #hexArr = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
    try:
        avgGenerationTime = (((timeChainGood[-1] - timeChainGood[0]))+(timeChainEvil[-1]-timeChainEvil[0]))/(len(timeChainGood)+len(timeChainEvil))
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
        if(len(timeChainEvil) >= len(timeChainGood)+1):
            return parentHash, None
        nonce += 1
        block = [parentHash, data, nonce]
        hash = hashlib.sha256(';'.join(map(str,block)).encode('utf-8')).hexdigest()
        AutoAdjustDifficulty()
    epoch = time.time() #int(calendar.timegm(time.gmtime())) #Time in seconds since epoch
    return hash, epoch
        
def getRandData():
    #time.sleep(BlockLength)
    return random.random()*10000000000 + random.random()*100000000

#Run the stuff
def startThreadEvil():
    global parentHashEvil, timeChainEvil, timeChainGood, evilPrinted
    #print("Starting Evil")
    tim = 0
    while(len(timeChainEvil) <= len(timeChainGood)+1):
        data = getRandData()
        parentHashEvil, tim = MakeBlock(parentHashEvil, data)
        if(tim != None):
            timeChainEvil.append(tim)
            #print(tim)
        else:
            return
        #if(len(timeChainEvil)%5==0): 
        AutoAdjustDifficulty()
    if(not evilPrinted):
        evilPrinted = True
        #print("Evil:",timeChainEvil)

def startThreadGood():
    global parentHashGood, timeChainGood, timeChainEvil, goodPrinted
    #print("Starting Good")
    tim = 0
    while(len(timeChainEvil) <= len(timeChainGood)+1):
        data = getRandData()
        parentHashGood, tim = MakeBlock(parentHashGood, data)
        if(tim != None):
            timeChainGood.append(tim)
            #print(tim)
        else: return
        #if(len(timeChainGood)%5==0): 
        AutoAdjustDifficulty()
    if(not goodPrinted):
        goodPrinted = True
        #print("Good:",timeChainGood)
    

def eventLoop(numGood=7, numThreads = 10): 
    global timeChainEvil, timeChainGood
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
    try:
        return timeChainEvil[-1]-timeChainGood[0], avgGenerationTime
    except:
        return timeChainEvil[0]-timeChainGood[0], avgGenerationTime

    return ("Good: %d"%(numGood),timeChainGood, "Evil: %d"%(numThreads-numGood), timeChainEvil)

runs = 10
Difficulty = "0" 
NumGThreads = 4
DifThreads = {}
def getStatData():
    global DifThreads, NumGThreads, Difficulty, runs
    for j in range(5):#numDifficulties
        GThread = [[1],[2],[3],[4],[5],[6]]
        GenTime = [[1],[2],[3],[4],[5],[6]]
        for i in GThread[:NumGThreads]:
            print("#Good:", i[0])
            for j in range(runs):
                try:
                    x, y = eventLoop(numGood = i[0])
                    i.append(x)
                    GenTime[i[0]].append(y)
                except:
                    pass
                resetGlobals()
        DifThreads[Difficulty] = (GThread, GenTime)
        Difficulty = ''.join([Difficulty,"0"])
getStatData()
print(DifThreads)
