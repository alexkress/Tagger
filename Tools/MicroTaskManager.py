from sms import SMS
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
 
    IdName_Dict[workerId] = workerName
    IdPhone_Dict[workerId] = workerPhone
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
    sentenceText  = elements[1] 
 
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
    PendingWork_Dict[workerId] = sentenceId
    IdStatus_Dict[workerId] = 'Working'
    IdSentCount_Dict[sentenceId] += 1
    print "Attributed: " + str(sentenceId) + " to " + IdName_Dict[workerId]

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
    receivedMsg = ReceiveSMS()
    
    #for msg in receivedMsg:
    #    print msg


