from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

     url(r'^$', 'gameapp.views.index'),
     url(r'^select', 'gameapp.views.select'),
     url(r'^play/(?P<gameid>\d{1})', 'gameapp.views.play'),
     url(r'^talk/(?P<gameid>\d{1})', 'gameapp.views.talk'),
     url(r'^game/(?P<gameid>\d{1})', 'gameapp.views.game'),
	 url(r'^result', 'gameapp.views.result'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

if settings.DEBUG:
	urlpatterns += patterns('',
		url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	)