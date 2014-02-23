from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

from .views import HomePageView, EventPageView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smapchat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^event/1$', EventPageView.as_view(), name='event'),
    url(r'^event/1.json$', 'smapchat.views.event_json', name='event_json'),
    url(r'^mail/test$', 'smapchat.views.send_mail', name='send_mail')
)
