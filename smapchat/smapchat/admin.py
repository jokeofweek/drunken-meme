from django.contrib import admin
from smapchat.models import UserProfile, Event, Map

admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Map)
