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
from settings import API_KEYS

from smapchat.models import Event, UserProfile, User

class HomePageView(TemplateView):
    template_name = 'home.html'

class EventPageView(TemplateView):
    template_name = 'event.html'

class UserPopoverView(TemplateView):
    template_name = 'popover.html'

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

    try:
            profile = request.user.get_profile()
            pp = pprint.PrettyPrinter(indent=4)
            profile.phone = request.POST['phoneinput']
            pp.pprint(request.POST['pref'])
            profile.pref = (request.POST['pref']=="email")
            pp.pprint(profile.pref)
            profile.save()
    except Exception:
        pass 
             

    context = {}
    if request.user.is_authenticated():
        try:
            access = request.user.accountaccess_set.all()[0]
        except IndexError:
            access = None
        else:
            client = access.api_client
            context['info'] = client.get_profile_info(raw_token=access.access_token)
            context['phone'] = request.user.get_profile().phone
            context['pref'] = request.user.get_profile().pref
    return render(request, "profile.html", context)

@login_required
def usersinfo(request):
    profileslist = UserProfile.objects.all()[:]
    context = {'profileslist': profileslist}
    try:
        return render(request, "usersinfo.html", context)
    except Exception:
        return HttpResponse("whoops")

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

@login_required
def user_json(request, userId):
    try :
        profile = UserProfile.objects.get(user_id=userId)
        json_obj = {
            'type': 'user',
            'id': userId,
            'full_name': profile.full_name,
            'username': profile.user.username
        }
        return HttpResponse(json.dumps(json_obj), content_type="application/json")
    except ObjectDoesNotExist:
        return HttpResponseNotFound(json.dumps({'type': 'error'}), content_type="application/json")

def send_mail(request):
    user = API_KEYS['SG_USER']
    pw = API_KEYS['SG_PASS']
    reciever = request.POST['to']
    subject = request.POST['subject']
    body = request.POST['body']
    sg = sendgrid.SendGridClient(user, pw)
    message = sendgrid.Mail()
    message.add_to(reciever)
    message.set_subject(subject)
    message.set_html(body)
    message.set_text(body)
    message.set_from(request.user.get_profile().email)
    print (sg.send(message))
    return HttpResponse(reciever)

def send_text(request):
    account_sid = API_KEYS["TWILIO_SID"]
    auth_token = API_KEYS["TWILIO_AUTH"]
    txtfrom = API_KEYS["TWILIO_NUM"]
    body = request.POST['body']
    txtto = request.POST['to']
    client = TwilioRestClient(account_sid, auth_token)

    message = client.sms.messages.create(body=body,
        to=txtto,    # Replace with your phone number
            from_=txtfrom) # Replace with your Twilio number
    print message.sid
    return HttpResponse("Sent a text to " + txtto +"!")

