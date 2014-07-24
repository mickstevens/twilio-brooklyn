# Title: Twilio Voice App Control via SMS
# Author: Mick Stevens
# Contact: +44 20 3095 6505 / mickstevens@yahoo.com
# Version: Extreme draft!
# Notes: My first off piste Twilio hack! Python newbie alert!
# Dedicated to @dN0T, @rickyrobinett, @phalt_, @mattmakai & @ryan_horn & many other Twilio'ers for INSPIRATIONAL BLOGGING!
# All constructive feedback from the Pythonista community welcome (be nice! :)    )

from flask import Flask
from flask import request
from twilio import twiml
from twilio.rest import TwilioRestClient

app = Flask(__name__)

# 1) haven't quite finished the authentication of request based on cli yet...
callers = {"+Number": "Name"}

@app.route('/callfwd', methods=['POST'])
def callfwd():
    account_sid = "ACxxxxxxxxxxxxxxxxxxxxxx"
    auth_token  = "12345678901234567890etc"
    client = TwilioRestClient(account_sid, auth_token)
# 2) ditto 1) above next 5 lines
#    from_number = request.values.get('From', None)
#    if from_number in callers:
#        caller = callers[from_number]
#    else:
#        caller = "Monkey"
# 3) twimil.Response().message not working as desired when tested, using message = client.message.create below instead
#    response = twiml.Response()
    # Collect the body of the text message from the user.
    body = request.form['Body']

    # If user sends BROWSER in the text message, set Twilio number to Twilio Client App
    if "BROWSER" in body.upper():
    	browser = client.phone_numbers.update("PNxxxxxxxxxxyyyyyyyyyy", voice_application_sid="APyyyyyyyyyyxxxxxxxxxx")
        message = client.messages.create(to="+to_number", from_="+from_number",body="Your Twilio No. is being routed to your Twilio Client.")
        print "Ahoy, You can make & receive calls in your browser, no phone, no 3rd party Apps, how cool is that!"
# 4) see 3) above
#        response.message("Your Twilio No. is set to deliver calls to your Twilio Client.")
    # If user sends FORWARD in the text message, set Twilio number to CallFwdMob App
    elif "FORWARD" in body.upper():
        forward = client.phone_numbers.update("PNxxxxxxxxxxyyyyyyyyyy", voice_application_sid="APxxxxxxxxxxyyyyyyyyyy")
        message = client.messages.create(to="+441234567890", from_="+1234567890",body="Your Twilio No. is being diverted to your mobile.")
        print "Ahoy, Your Twilio No. is being diverted to your mobile, as requested."
    # If no preference, or nonsense, received set Twilio number to vmail.
    else:
        vmail = client.phone_numbers.update("PNxxxxxxxxxxyyyyyyyyyy", voice_application_sid="APxxxxxxxxxxyyyyyyyyyy")
        message = client.messages.create(to="+1234567890", from_="+1234567890",body="Calls to your Twilio No. are being sent to voicemail.")
        print "Ahoy, Your Twilio No. is routing to your voicemail, enjoy your lunch in peace."
    return 'some response' #frigs python newbie "view function did not return a response error" feedback from pythonistas welcome!

if __name__ == "__main__":
    # Since this is a development project, we will keep debug on to make our
    # lives easier. We would want to configure our app more conservatively
    # in production.
    app.debug = True
    app.run()
