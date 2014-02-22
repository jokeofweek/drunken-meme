import json

from django.http import HttpResponse


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
    return HttpResponse("Hey", content_type="text/html")
