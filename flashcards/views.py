from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.base import View
from flashcards.models import *

class view_decks(View):
    template_name = "flashcards/view_decks.html"
    def get(self, request):
        decks = Deck.objects.all()
        return render(request, self.template_name, locals())

class deck(View):
    template_name = "flashcards/view_single_deck.html"
    time = None
    def get(self, request, deck_id):
        decks = Deck.objects.all()
        cards = Card.objects.filter(deck=deck_id)
        deck = Deck.objects.get(pk=deck_id)
        time = timezone.now()
        return render(request, self.template_name, locals())

def right(request, card_id):
        card = Card.objects.get(pk=card_id)
        card.asked += 1
        card.save()
        return HttpResponse()

def wrong(request, card_id):
        card = Card.objects.get(pk=card_id)
        card.asked += 1
        card.wrong += 1
        card.save()
        return HttpResponse()

class create_deck(View):
    template_name = "flashcards/create_deck.html"
    def get(self, request):
        return render(request, self.template_name, locals())

    def post(self, request):
        print("hallo")
        
