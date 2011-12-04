from sms import SMS
from evaluation import evaluation, Evaluator, Stats
import sys
import os
import time
from textualui import TextualUI
import optparse

sms = SMS()
workerFile = '../Data/workerList.txt'
sentenceFile = '../Data/sentenceList.txt'
responseFile = '../Data/responseList.txt'

fake_message_sending=True

#Information used for the demo stored in dictionnaries
#Once we have a database, all this informaton will be obtained/stored
#via DB interface...
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

    #print workerName


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

    #print sentenceText


def find_key(dic, val):
    for k,v in dic.iteritems():
        if v == val:
            return k
    return -1;

#Retrieve workerId given it's phone number (-1 if not found)
def GetWorkerFromPhone(phoneNmb):
    return find_key(IdPhone_Dict, phoneNmb); 

#Retrieve Idle Worker (-1 if not found)
def GetIdleWorker():
    return find_key(IdStatus_Dict, 'Idle');


#Get the Id of a sentence that need to be tagged, but has
# not already been tagged by the specified worker.
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
    #print "Attributed: " + str(sentenceId) + " to " + IdName_Dict[workerId]
    TextualUI.ShowOutgoingMessage(IdPhone_Dict[workerId], IdName_Dict[workerId], IdSentence_Dict[sentenceId])


#Change the state of a worker so it will received new data
def AcknowledgeSentenceTagged(workerId, isOk):
    del PendingWork_Dict[workerId]
    IdStatus_Dict[workerId] = 'Idle'
    if(isOk):
        pass
        #print 'Sentence Successfully tagged'


def SendWorkUnits(workCount):
    if workCount < 1:
        return
    for x in range(workCount):
        workerId = GetIdleWorker()
        if(workerId == -1):
            #print 'No Idle Worker'
            break
        #Give work to this worker...
        sentenceId = GetNewSentenceToTag(workerId)
        if(sentenceId == -1):
            #print 'No idle sentence'
            break
        
        #Try Sending SMS to worker
        if(fake_message_sending or sms.send(IdSentence_Dict[sentenceId], IdPhone_Dict[workerId]) ):
            #Successfully Send SMS, Add Sentece/Worker to waiting queue.
            AttributeSentenceToWorker(sentenceId,workerId)
        else:
            print 'Unable to send Msg to: ' + IdName_Dict[workerId]        
            

def ProcessReceivedMessages(workUnitToProcess, quiet=False):
    #Contact Server to receive SMS
    receivedMsg = sms.receive(workUnitToProcess)
    
    for msg in receivedMsg:
        sourcePhone = msg.get_source().strip()
        msgBody = msg.get_body().strip()
        #msgDate = msg.get_date_sent()

        #Check which person has send this message...
        workerId = GetWorkerFromPhone(sourcePhone)
        if(workerId == -1):
            if not quiet:
                print 'Unknown phone source... ' + sourcePhone
            continue
        
        if workerId not in PendingWork_Dict:
            if not quiet:
                print "Error: Received answer from Worker not active"
            continue

        worker_name=IdName_Dict[workerId]

        if not quiet:
            TextualUI.ShowIncomingMessage(msg,worker_name)
        #print "Received " + msg.get_body() + " from " + IdName_Dict[workerId]

        originalSentId = PendingWork_Dict[workerId]
        original_sentence=IdSentence_Dict[originalSentId]

        '''
        if(evaluation( original_sentence, msgBody) ):
            AcknowledgeSentenceTagged(workerId,True)

            if not quiet:
                TextualUI.ShowProcessedResult(msg, worker_name, original_sentence, True)
            #Push Results to DataBase
            #Free Worker for further work
        '''
        Ev = Evaluator()
        if(Ev.evaluation( original_sentence, msgBody) ):
            AcknowledgeSentenceTagged(workerId,True)

            if not quiet:
                TextualUI.ShowProcessedResult(msg, worker_name, original_sentence, True)

            #Push Results to DataBase
            Ev.push(responseFile, originalSentId, workerId)
            
            #Free Worker for further work
                
        else:
            AcknowledgeSentenceTagged(workerId,False)
            if not quiet:
                TextualUI.ShowProcessedResult(msg, worker_name, original_sentence, False)


            #print 'Worker did not tagged the sentence properly'
            #print  IdSentence_Dict[originalSentId] + " -> " + msgBody
            

S = Stats()
St.format(sentenceFile, sentenceFile) 

#data per word is held in S.data 

### Main Loop ###


if __name__=="__main__":
    parser = optparse.OptionParser("usage: %prog arg")
    parser.add_option("-s", "--send", dest="send",
                default="No", type="string",
                help="specify whether to send out messages")

    (options, args) = parser.parse_args()

    if len(args) > 1:
        parser.error("incorrect number of arguments")
        
    fake_message_sending = (False if options.send=="Yes" else True)

    #How many SMS we want to send each time...
    workUnitsToCreate = 2
    workUnitsToProcess = 2

    TextualUI.StartUI()

    ProcessReceivedMessages(10000, True)

    while(True):
        time.sleep(1)
        # Attribute Sentence to Tag to Idle Workers
        SendWorkUnits(workUnitsToCreate)

        # Get Received SMS and attribute if correctly answered
        ProcessReceivedMessages(workUnitsToProcess)



