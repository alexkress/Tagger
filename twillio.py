# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="sasha"
__date__ ="$Dec 3, 2011 12:04:18 PM$"

from twilio.rest import TwilioRestClient

from Tools.sms import SMS

sms=SMS()
print sms.send("hello", "+14165431525")

msgs=sms.receive()

for msg in msgs:
    print "Received "+msg.get_body()+" from "+msg.get_source()

if __name__ == "__main1__":
    account = "ACf3a4c18fb6b24d01a99aa2770c187900"
    token = "d83d9fb72dd8a2fbe04c112ec6fe2577"
    client = TwilioRestClient(account, token)

    #message = client.sms.messages.create(to="+16477719022", from_="+14155992671",
    #                                 body="Hello from the Montreal team, to reply type 5370-3238 before your message")

    msgs=client.sms.messages.list()


    
    print a
    for message in a:
        print dir(message)
        #message.delete_instance(message.sid)
        print message.name
        print message.date_sent
        print message.body
        print message.base_uri
        print message.from_
        print message.to
        print message.sid
        print message.status
        print "----"