from django.conf.urls import patterns, url
from .views import view_decks, deck

urlpatterns = patterns('',
    url(r'^$', view_decks.as_view(), name='index'),
    url(r'^(?P<deck_id>\d+)/$', deck.as_view(), name='deck_view'),
)
