# Title: Twilio Voice App Control via SMS
# Author: Mick Stevens
# Contact: +44 20 3095 6505 / mickstevens@yahoo.com
# Version: 2
# Notes: My first off piste Twilio hack! Python newbie alert!
# Dedicated to @dN0T, @rickyrobinett, @phalt_, @mattmakai & @ryan_horn & many other Twilio'ers for INSPIRATIONAL BLOGGING!
# All constructive feedback from the Pythonista community welcome (be nice! :)    )

from flask import Flask
from flask import request, redirect
from twilio import twiml
from twilio.rest import TwilioRestClient
import os

app = Flask(__name__)
# app.config.from_pyfile('local_settings.py') #

#Perform authenticaton via CallerID, prevents other changing your active Twilio VoiceUrl 
#Needs to be a Twilio verifed No. (for trial accounts only)

callerId = {"+1234567890": "Your Name"}

@app.route("/auth", methods=['GET', 'POST'])
def authenticate(): 
    from_number = request.values.get('From', None)
    if from_number in callerId:
        return redirect("/callctrl")
    else:
        message = "401 Unauthorized."

    resp = twiml.Response()
    resp.message(message)
 
    return str(resp)

@app.route('/callctrl', methods=['POST'])
def callctrl():
    account_sid = "AC******************************"
    auth_token  = "********************************"
    ap1_sid = "AP******************************" # e.g. your Twilio Client App SID
    ap2_sid = "AP******************************" # e.g. your CallFwd to Mobile App SID
    ap3_sid = "AP******************************" # e.g. your Vmail then Email Msg SID
    body = request.form['Body']
    client = TwilioRestClient(account_sid, auth_token)
    mobile = "+1234567890"
    pn_sid = "PN******************************"
    resp = twiml.Response()
    twilio_no = "+19876543210"

# If user sends CLIENT in the text message, set Twilio number to Twilio Client App

    if "CLIENT" in body.upper():
    	browser = client.phone_numbers.update(pn_sid, voice_application_sid=ap1_sid)
        message = client.messages.create(to=mobile, from_=twilio_no,body="Your Twilio No. is being routed to your Twilio Client.")
        print "Ahoy Hoy! You can make & receive calls in your browser, no phone, no 3rd party Apps, how cool is that!"
    
# If user sends FORWARD in the text message, set Twilio number to CallFwdMob App

    elif "CALLFWD" in body.upper():
        forward = client.phone_numbers.update(pn_sid, voice_application_sid=ap2_sid)
        message = client.messages.create(to=mobile, from_=twilio_no,body="Your Twilio No. is being diverted to your mobile.")
        print "Ahoy Hoy! Your Twilio No. is being diverted to your mobile, as requested."

# If no preference, or nonsense, received set Twilio number to vmail.

    else:
        vmail = client.phone_numbers.update(pn_sid, voice_application_sid=ap3_sid)
        message = client.messages.create(to=mobile, from_=twilio_no,body="Calls to your Twilio No. are being sent to voicemail.")
        print "Ahoy Hoy! Your Twilio No. is routing to your voicemail, enjoy your lunch in peace."
    
    return str(resp) 

if __name__ == "__main__":
    # Since this is a development project, we will keep debug on to make our
    # lives easier. We would want to configure our app more conservatively
    # in production.
    app.debug = False
    app.run()
