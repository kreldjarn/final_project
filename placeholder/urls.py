from django.conf.urls import patterns, url

from placeholder import views

urlpatterns = patterns('',
    url(r'^$', views.hello, name='hello'),
)
