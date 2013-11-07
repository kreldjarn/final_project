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
    def get(self, request, deck_id):
        return HttpResponse("test %s", deck_id)
