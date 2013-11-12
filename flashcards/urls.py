from django.conf.urls import patterns, url
from .views import view_decks, deck, right, wrong, create_deck

urlpatterns = patterns('',
    url(r'^$', view_decks.as_view(), name='index'),
    url(r'^(?P<deck_id>\d+)/$', deck.as_view(), name='deck_view'),
    url(r'^(?P<card_id>\d+)/rett/$', right, name='right'),
    url(r'^(?P<card_id>\d+)/rangt/$', wrong, name='wrong'),
    url(r'^create/$', create_deck.as_view(), name='create_deck'),
)
