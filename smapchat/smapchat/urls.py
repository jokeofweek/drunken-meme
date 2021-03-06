from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

from .views import HomePageView, EventPageView, CustomRedirect, CustomCallback, SuccessPageView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smapchat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/', include('allaccess.urls')),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^success$', SuccessPageView.as_view(), name='success'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^contact/(?P<userId>[0-9]+)$', 'smapchat.views.usersinfo', name='usersinfo'),
    url(r'^event/(?P<eventId>[0-9]+)$', login_required(EventPageView.as_view()), name='event'),
    url(r'^event/(?P<eventId>[0-9]+).json$', 'smapchat.views.event_json', name='event_json'),
    url(r'^user/(?P<userId>[0-9]+).json$', 'smapchat.views.user_json', name='user_json'),
    url(r'^user/(?P<userId>[0-9]+)$', 'smapchat.views.popover', name='popover'),
    url(r'^contact-dialog/(?P<userId>[0-9]+)$', 'smapchat.views.contact_dialog', name='contact_dialog'),
    url(r'^send$', 'smapchat.views.send', name='send'),
    url(r'^send/mail$', 'smapchat.views.send_mail', name='send_mail'),
    url(r'^send/text$', 'smapchat.views.send_text', name='send_text'),
    url(r'^logout$', 'django.contrib.auth.views.logout',  {'next_page': '/'}),
    url(r'^join$', 'smapchat.views.join',  name='join'),
    url(r'^profile/$', 'smapchat.views.profile', name='profile'),
    url(r'^login$', RedirectView.as_view(url='/login/facebook'), name='login-root'),
    url(r'^login/(?P<provider>(\w|-)+)/$', CustomRedirect.as_view(), name='login'),
    url(r'^callback/(?P<provider>(\w|-)+)/$', CustomCallback.as_view(), name='callback'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

