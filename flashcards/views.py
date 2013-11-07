from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from flashcards.models import *

def view_decks(request):
    template_name = "flashcards/view_decks.html"
    decks = Deck.objects.all()
    return render(request, template_name, locals())

def deck_view(request, deck_id):
    return HttpResponse("test %s", deck_id)
