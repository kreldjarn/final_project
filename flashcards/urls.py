from django.conf.urls import patterns, url
from .views import view_decks, deck, create_deck, create_cards, edit_card

urlpatterns = patterns('',
    url(r'^$', view_decks.as_view(), name='index'),
    url(r'^(?P<deck_id>\d+)/$', deck.as_view(), name='deck_view'),
    url(r'^create/$', create_deck.as_view(), name='create_deck'),
    url(r'^create/(?P<deck_id>\d+)/$', create_cards.as_view(), name="create_card"),
    url(r'^edit/$', edit_card.as_view(), name="edit_card"),
    url(r'^delete/(?P<card_id>\d+)', edit_card.as_view(), name="delete_card"),
    
)
