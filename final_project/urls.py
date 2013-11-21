from django.conf.urls import patterns, include, url
from .views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('flashcards.urls')),
    
    url(r'^admin/', include(admin.site.urls)),

    url(r'^account/login/$', login),
    url(r'^account/authenticate/$', auth_view),
    url(r'^account/logout/$', logout),
    url(r'^account/logged/$', logged),
    url(r'^account/invalid/$', invalid),

    url(r'^account/register/$', register.as_view()),
    url(r'^account/success/$', success),
)
