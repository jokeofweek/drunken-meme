from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

from .views import HomePageView, EventPageView, ProviderLoginView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smapchat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/', include('allaccess.urls')),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^event/1$', EventPageView.as_view(), name='event'),
    url(r'^event/1.json$', 'smapchat.views.event_json', name='event_json'),
    url(r'^send/mail$', 'smapchat.views.send_mail', name='send_mail'),
    url(r'^send/text$', 'smapchat.views.send_text', name='send_text'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^accounts/login/$', RedirectView.as_view(url='/accounts/login/facebook', permanent=False), name='index'),
    url(r'^accounts/profile/$', 'smapchat.views.profile', name='profile'),
    url(r'^accounts/login/(?P<provider>(\w|-)+)/$', ProviderLoginView.as_view(), name='login-callback'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

