from sms import SMS
from evaluation import evaluation
import sys
import os
import time

sms = SMS()
workerFile = '../Data/workerList.txt'
sentenceFile = '../Data/sentenceList.txt'


IdName_Dict = dict()
IdPhone_Dict = dict()
IdStatus_Dict = dict()
IdSentDone_Dict = dict()

#Read the list of User from a file and put them in a dictionnary
wf = open(workerFile)
lines = wf.readlines()
workerToProcess = len(lines)

for line in lines:
    #Remove end of lines
    line = line.strip()
    #Erase info after # on a line
    if line.find('#') != -1:
        line = line[1:line.find('#')]
    #Separate Elements
    elements = line.split(',')
    if len(elements) != 3:
        continue

    workerId    = int(elements[0])
    workerName  = elements[1] 
    workerPhone = elements[2]
 
    IdName_Dict[workerId] = workerName.strip()
    IdPhone_Dict[workerId] = workerPhone.strip()
    IdStatus_Dict[workerId] = 'Idle' 
    IdSentDone_Dict[workerId] = list() 

    print workerName


# Read a list of sentence from a file
f = open(sentenceFile)
lines = f.readlines()
sentencesToProcess = len(lines)

IdSentence_Dict = dict()
IdSentCount_Dict = dict()
MaxSentIteration = 3;

for line in lines:
    #Remove end of lines
    line = line.strip()
    #Erase info after # on a line
    if line.find('#') != -1:
        line = line[1:line.find('#')]
    #Separate Elements
    elements = line.split('@,')
    if len(elements) != 2:
        continue

    sentenceId    = int(elements[0])
    sentenceText  = elements[1].strip()
 
    IdSentence_Dict[sentenceId] = sentenceText
    IdSentCount_Dict[sentenceId] = 0

    print sentenceText

def ReceiveSMS():
    return [1,2,3];

def SendSMS(phoneNumber, TextSentence):
    return True;

def find_key(dic, val):
    for k,v in dic.iteritems():
        if v == val:
            return k
    return -1;

#Retrieve Idle Worker
def GetWorkerFromPhone(phoneNmb):
    idleWorkerId = -1
    idleWorkerId = find_key(IdPhone_Dict, phoneNmb);
 
    return idleWorkerId

#Retrieve Idle Worker
def GetIdleWorker():
    idleWorkerId = -1
    idleWorkerId = find_key(IdStatus_Dict, 'Idle');
    return idleWorkerId

#Get the Id of a sentence not tagged by the worker.
# If none is found, return -1
def GetNewSentenceToTag(workerId):
    for k, v in IdSentence_Dict.iteritems():
        if( IdSentDone_Dict[workerId].count(k) == 0 and
            IdSentCount_Dict[k] < MaxSentIteration):
            return k
    return -1

#Dictionnary matching workerID to sentence attributed to the
# worker...
PendingWork_Dict = dict()

#Retrieve Idle Worker
def AttributeSentenceToWorker(sentenceId,workerId):
    #Specify the current sentence a worker is working on
    PendingWork_Dict[workerId] = sentenceId
    #Set the status of worker as occupied
    IdStatus_Dict[workerId] = 'Working'
    #Count number of time each sentence was sent to a worker
    IdSentCount_Dict[sentenceId] += 1
    #Make sure Worker do not received same sentence twice
    IdSentDone_Dict[workerId].append(sentenceId)
    print "Attributed: " + str(sentenceId) + " to " + IdName_Dict[workerId]

def AcknowledgeSentenceTagged(workerId, isOk):
    del PendingWork_Dict[workerId]
    IdStatus_Dict[workerId] = 'Idle'
    if(isOk):
        print 'Sentence Successfully tagged'

while(True):
    time.sleep(1)
    # Attribute Sentence to Tag to Idle Workers
    workerId = GetIdleWorker()
    if(workerId != -1):
        #Give work to this worker...
        sentenceId = GetNewSentenceToTag(workerId)
        if(sentenceId != -1):
            if(sms.send(IdSentence_Dict[sentenceId], IdPhone_Dict[workerId]) ):
                #Successfully Send SMS, Add Sentece/Worker to waiting queue.
                AttributeSentenceToWorker(sentenceId,workerId)
            else:
                print 'Unable to send Msg to: ' + IdName_Dict[workerId]
    # Get Received SMS and attribute if correctly answered
    receivedMsg = sms.receive(1)
    
    for msg in receivedMsg:
        sourcePhone = msg.get_source().strip()
        msgBody = msg.get_body().strip()
        print "Received " + msg.get_body() + " from " + msg.get_source()
        
        #Check which person has send this message...
        workerId = GetWorkerFromPhone(sourcePhone)
        if(workerId == -1):
            print 'Unknown phone source... ' + sourcePhone 
            continue
        
        if workerId not in PendingWork_Dict:
            print "Worker not assigned any Data"
            continue

        originalSentId = PendingWork_Dict[workerId]
        
        if(evaluation( IdSentence_Dict[originalSentId], msgBody) ):
            AcknowledgeSentenceTagged(workerId,True)
            #Push Results to DataBase
            #Free Worker for further work
        else:
            AcknowledgeSentenceTagged(workerId,False)
            print 'Worker did not tagged the sentence properly'
            print  IdSentence_Dict[originalSentId] + " -> " + msgBody
            

    #for msg in receivedMsg:
    #    print msg


