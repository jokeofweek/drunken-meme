import pprint
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from django.db.models.signals import post_save

     
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)  
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    pref = models.BooleanField()
    def get_full_name(self):
        # The user is identified by their email address
        return self.full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Event(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)

class Map(models.Model):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    event = models.ForeignKey(Event)

# Register a handler for the post_save signal
# Otherwise the user profile does not get created
post_save.connect(create_user_profile, sender=User)
