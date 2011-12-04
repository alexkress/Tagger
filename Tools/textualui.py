# To change this template, choose Tools | Templates
# and open the template in the editor.

import sms
import time
from time import gmtime, strftime

strSpace = 5 *" "

class TextualUI:

    @staticmethod
    def GetTimeStamp():
        return time.strftime("[%H:%M:%S]", gmtime())

    @staticmethod
    def StartUI():
        print "WELCOME TO TAGGER"
        print "------------------"

    @staticmethod
    def ShowErrorMessage(content):
        print TextualUI.GetTimeStamp() + "?? " + content

    @staticmethod
    def ShowOutgoingMessage(number, name, content):
        print TextualUI.GetTimeStamp() + "-> Asking "+name+" to tag: \'"+content+"\'"
    
    @staticmethod
    def ShowIncomingMessage(msg, name):
        print TextualUI.GetTimeStamp() + "<- Received new message \'"+str(msg.get_body())+"\' from "+name #+" at "+ msg.get_date_sent()

    @staticmethod
    def ShowProcessedResult(msg, name, original_sentence, correct):
        outStr = "*"+name + (' correctly' if correct else ' incorrectly') + " tagged \'" + original_sentence+ "\' as " + msg.get_body()
        printedChr = 0
        maxLength = 80
        while(printedChr < len(outStr)):
            if len(outStr[printedChr:]) < maxLength:
                print strSpace + outStr[printedChr:]
                break
            else:
                lastSpace = outStr[printedChr:printedChr+maxLength].rfind(' ')
                print strSpace + outStr[printedChr:printedChr+lastSpace]
                printedChr += lastSpace

    @staticmethod
    def ShowEvaluationMessage(msg):
        print strSpace + "Evaluation: " +  msg
