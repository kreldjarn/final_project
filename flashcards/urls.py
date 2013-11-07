from django.conf.urls import patterns, url
from flashcards import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
