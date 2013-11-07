from django.conf.urls import patterns, url
from flashcards import views

urlpatterns = patterns('',
    url(r'^$', views.view_decks, name='index'),
    url(r'^(?P<deck_id>\d+)/$', views.deck_view, name='deck_view'),
)
