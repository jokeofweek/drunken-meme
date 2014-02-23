import json
import sendgrid
import os
import pprint
import hashlib
import base64

from django.core.urlresolvers import reverse
from twilio.rest import TwilioRestClient
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseNotFound
from allaccess.compat import get_user_model, smart_bytes, force_text
from allaccess.views import OAuthCallback, OAuthRedirect
from jsonview.decorators import json_view
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from smapchat.models import Event

class HomePageView(TemplateView):
    template_name = 'home.html'

class EventPageView(TemplateView):
    template_name = 'event.html'

class CustomRedirect(OAuthRedirect):
    "Redirect to custom callback."

    def get_callback_url(self, provider):
        "Return the callback url for this provider."
        return reverse('callback', kwargs={'provider': provider.name})

    def get_additional_parameters(self, provider):
        # Request permission to see user's email
        return {'scope': 'email'}

class CustomCallback(OAuthCallback):
    "Create custom user on callback."

    def get_or_create_user(self, provider, access, info):
        "Create a shell custom.MyUser."
        username = info.get('username', None)
        email = info.get('email', None)
        name = info.get('name', None)
        if email is None:
            # No email was given by the provider so create a fake one
            digest = hashlib.sha1(smart_bytes(access)).digest()
            # Base 64 encode to get below 30 characters
            # Removed padding characters
            email = '%s@example.com' % force_text(base64.urlsafe_b64encode(digest)).replace('=', '')
        User = get_user_model()
        """
        kwargs = {
            'email': email,
            'full_name': name,
            'password': None
        }
        """
        u = User.objects.create_user(username, email, None)
        profile = u.get_profile()
        profile.email = email
        profile.full_name = name
        profile.save()
        return u


@login_required
def profile(request):
    context = {}
    if request.user.is_authenticated():
        try:
            access = request.user.accountaccess_set.all()[0]
        except IndexError:
            access = None
        else:
            client = access.api_client
            context['info'] = client.get_profile_info(raw_token=access.access_token)
    return HttpResponse(pprint.pformat(context))

@login_required
def join(request):
    if request.user.is_authenticated():
        eventlist = Event.objects.filter()
        context = {'eventlist': eventlist}
        try:
            return render(request, "join.html", context)
        except IndexError:
            return HttpResponse("index error")
        except Exception:
            return HttpResponse("error")
    else:
        return HttpResponse("stupid")

    eventlist = Event.objects.filter()
    template = loader.get_template('join.html')
    context = {'eventlist': eventlist}
    return render(request, 'test.html', context)


@login_required
def event_json(request, eventId):
    try :
        obj = Event.objects.get(pk=eventId)
        json_obj = {
            'type': 'event',
            'id': obj.id,
            'name': obj.name,
            'desc': obj.desc,
            'maps': map(lambda x: {
                'name': x.name,
                'source': x.source
            }, obj.map_set.order_by('pk')[:])
        }
        return HttpResponse(json.dumps(json_obj), content_type="application/json")
    except ObjectDoesNotExist:
        return HttpResponseNotFound(json.dumps({'type': 'error'}), content_type="application/json")

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

