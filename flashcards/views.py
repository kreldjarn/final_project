from django.http import HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone
from django.core import serializers
from django.views.generic.base import View
from flashcards.models import *
import json

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

    def post(self, request, deck_id):
        card_id = deck_id
        card = Card.objects.get(pk=card_id)
        card.asked += 1
        ans = request.POST.get("svar")
        if (ans == "rangt"):
            card.wrong +=1
        card.save()
        return HttpResponse()

class create_deck(View):
    template_name = "flashcards/create_deck.html"
    def get(self, request):
        return render(request, self.template_name, locals())

    def post(self, request):
        objects = []
        if request.POST.get("stafli"):
            for o in serializers.deserialize("json", request.POST.get("stafli")):
                o.save()
                objects.append(o.object)
                # Hack til thess ad itra yfir eitt stak i Generator Iterable
                # Viljum ekki ad notandi geti submittad fleiri en einum stafla
                # per POST-adgerd.
                break
            return HttpResponse(serializers.serialize('json', objects), content_type='application/json')
        elif request.POST.get("spjald"):
            for o in serializers.deserialize("json", request.POST.get("spjald")):
                if (o.object.question and o.object.answer):
                    o.save()
                    objects.append(o.object)
            return HttpResponse(serializers.serialize('json', objects), content_type='application/json')


class create_cards(View):
    template_name = "flashcards/create_cards.html"
    def get(self, request, deck_id):
        currentDeck = get_object_or_404(Deck, pk=deck_id)
        cards = Card.objects.filter(deck=currentDeck)
        print(currentDeck)
        print(cards)
        return render(request, self.template_name, locals())

    # Notum POST-adferdina i create_deck einnig fyrir create_cards

class edit_card(View):
    def post(self, request, card_id):
        #card = Card.objects.get(id=card_id)
        #card.active = False
        #card.save()

        data = request.POST.get("spjald")
        if data:
            spjald = json.loads(data)
            print(spjald)
            return HttpResponse()
        data = request.POST.get("visible")
        if data:
            visible = json.loads(data)
            print(visible)
            return HttpResponse()
        data = request.POST.get("active")
        if data:
            active = json.loads(data)
            print(active)
            return HttpResponse()
        return HttpResponse()
