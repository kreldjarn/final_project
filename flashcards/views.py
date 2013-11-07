from django.http import HttpResponse
from flashcards.models import *

def index(request):
    return HttpResponse("test")

def deck_view(request, deck_id):
    decks = Deck.objects.all()
