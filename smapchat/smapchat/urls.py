from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

from .views import HomePageView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smapchat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^event/1$', TemplateView.as_view(template_name="map.html")),
    url(r'^event/1.json$', 'smapchat.views.event_json', name='event_json')
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

