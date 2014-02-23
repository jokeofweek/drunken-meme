import json
import sendgrid
import os
from django.views.generic import TemplateView
from django.http import HttpResponse

class HomePageView(TemplateView):
    template_name = 'home.html'

class EventPageView(TemplateView):
    template_name = 'event.html'


def event_json(request):
    obj = {
        'id': 1,
        'name': "McHacks",
        'desc': 'A Hackathon at McGill',
        'maps': [
            {'name': 'ssmu-floor-1', 'source': 'img'}
        ]
    }
    return HttpResponse(json.dumps(obj), content_type="application/json")

def send_mail(request):
    user = request.GET['user']
    pw = request.GET['pass']
    reciever = request.GET['to']
    sender = request.GET['from']

    sg = sendgrid.SendGridClient(user, pw)
    message = sendgrid.Mail()
    message.add_to(reciever)
    message.set_subject('Example')
    message.set_html('Body')
    message.set_text('Body')
    message.set_from(sender)
    print (sg.send(message))
    return HttpResponse(user + " " + pw + " " + reciever + " " + sender)

def send_text(request):
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = request.GET['user']
    auth_token = request.GET['auth']
    body = request.GET['body']
    txtto = request.GET['to']
    txtfrom = request.GET['from']
    client = TwilioRestClient(account_sid, auth_token)

    message = client.sms.messages.create(body=body,
        to=txtto,    # Replace with your phone number
            from_=txtfrom) # Replace with your Twilio number
    print message.sid
    return HttpResponse("Sent a text to " + txtto +"!")

