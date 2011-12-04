from twilio.rest import TwilioRestClient

from Tools.sms import SMS
from Tools.textualui import TextualUI

sms=SMS()
print sms.send("hello", "+15143453456")

msgs=sms.receive()

for msg in msgs:
    TextualUI.ShowIncomingMessage(msg)

if __name__ == "__main1__":
    account = "ACf3a4c18fb6b24d01a99aa2770c187900"
    token = "d83d9fb72dd8a2fbe04c112ec6fe2577"
    client = TwilioRestClient(account, token)

    #message = client.sms.messages.create(to="+15143453456", from_="+14155992671",
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