from twilio.rest import TwilioRestClient
import shelve
import twilio

class SMS:
    """Used to send and receive SMS"""

    class FriendlySMSFacade:
        def __init__(self, sms):
            self.body=sms.body
            self.from_=sms.from_
            self.date_sent=sms.date_sent

        def get_body(self):
            return self.body

        def get_source(self):
            return self.from_

        def get_date_sent(self):
            return self.date_sent

        def __str__(self):
            return self.get_body()+" "+self.get_source()+" "+self.get_date_sent()

    SHELF_FILE_NAME="used_messages.saved"
    SHELF_STORAGE_KEY="used_messages"

    used_messages=[]

    shelf=None

    def __init__(self):
        #enter you https://www.twilio.com token here
        account = "ACf3a4c18fb6b24d01a99aa2770c187900"
        token = "d83d9fb72dd8a2fbe04c112ec6fe2577"
        self.client = TwilioRestClient(account, token)
        self.load_used()
        #print "sms init"

    def __del__(self):
        self.shelf[self.SHELF_STORAGE_KEY]=self.used_messages
        self.shelf.sync()
        #print self.shelf

    @classmethod
    def is_used(cls, msg):
        return msg.sid in cls.used_messages

    @classmethod
    def mark_as_used(cls, msg):
        if not cls.is_used(msg):
            cls.used_messages.append(msg.sid)
            cls.shelf[cls.SHELF_STORAGE_KEY]=cls.used_messages
            cls.shelf.sync()
            #print str(len(cls.used_messages)) + "--- marked used"

    @classmethod
    def load_used(cls):
        if cls.shelf==None:
            cls.shelf = shelve.open(cls.SHELF_FILE_NAME)
            if cls.shelf.has_key(cls.SHELF_STORAGE_KEY):
                cls.used_messages=cls.shelf[cls.SHELF_STORAGE_KEY]
                print "Loaded "+str(len(cls.used_messages))+" stored messages"
            

    def send(self, message, number):
        """ true if sending is successful"""
        try:
            msg = self.client.sms.messages.create(to=number, from_="+14155992671",
                body="Please tag:\n "+message+"\n to reply type 5370-3238 before your message \n valid symbols n pn aj v av pr c in")
        except twilio.TwilioRestException:
            print "OOPS: "+number+" is not registered"
            return False

        return msg.status == "sent" or msg.status == "queued"

    def receive(self, limit=None):
        """ List of not yet seen responses """
        all_messages=self.client.sms.messages.list()

        #print "Got "+str(len(all_messages))+" messages from server"

        count_received=0

        to_return=[]
        #go through all the messages
        for msg in all_messages:

            if msg.status == "received" and (not SMS.is_used(msg)):
                to_return.append(SMS.FriendlySMSFacade(msg))
                SMS.mark_as_used(msg)
                count_received=count_received+1
                #print "Found un processed incoming message"

                if (not limit==None) and count_received>=limit:
                    break

        return to_return