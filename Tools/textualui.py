# To change this template, choose Tools | Templates
# and open the template in the editor.

import sms

class TextualUI:

    @staticmethod
    def StartUI():
        print "WELCOME TO TAGGER"
        print "------------------"

    @staticmethod
    def ShowOutgoingMessage(number, name, content):
        print "!!!!!! Asking "+name+" at "+number+" to tag: \'"+content+"\'"
    
    @staticmethod
    def ShowIncomingMessage(msg, name):
        print "-----> Received new message \'"+str(msg.get_body())+"\' from "+name+" at "+msg.get_date_sent()

    @staticmethod
    def ShowProcessedResult(msg, name, original_sentence, correct):
        print "****** "+name + (' correctly' if correct else ' incorrectly') + " tagged \'" + original_sentence+ "\' as " + msg.get_body()