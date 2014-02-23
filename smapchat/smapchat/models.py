import pprint
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from django.db.models.signals import post_save

     
class UserProfile(models.Model):
    user = models.OneToOneField(User)  
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    

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


# Register a handler for the post_save signal
# Otherwise the user profile does not get created
post_save.connect(create_user_profile, sender=User)
