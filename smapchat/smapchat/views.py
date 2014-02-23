import json
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
    return HttpResponse("Hey")
