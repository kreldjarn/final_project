from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from flashcards.models import *

class view_decks(View):
    template_name = "flashcards/view_decks.html"
    def get(self, request):
        decks = Deck.objects.all()
        return render(request, self.template_name, locals())

class deck(View):
    template_name = "flashcards/view_single_deck.html"
    def get(self, request, deck_id):
        decks = Deck.objects.all()
        cards = Card.objects.filter(deck=deck_id)
        deck = Deck.objects.get(pk=deck_id)
        return render(request, self.template_name, locals())
