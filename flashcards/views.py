from django.http import HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone
from django.core import serializers
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from flashcards.models import *
import json

from braces.views import LoginRequiredMixin

def to_base(q, alphabet):
    if q < 0: raise ValueError, "must supply a positive integer"
    l = len(alphabet)
    converted = []
    while q != 0:
        q, r = divmod(q, l)
        converted.insert(0, alphabet[r])
    return "".join(converted) or '0'

def to36(q):
    return to_base(q, '0123456789abcdefghijklmnopqrstuvwxyz')

class view_decks(LoginRequiredMixin, View):
    template_name = "flashcards/view_decks.html"
    
    def get(self, request):
        decks = Deck.objects.all()
        return render(request, self.template_name, locals())

class deck(LoginRequiredMixin, View):
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

class create_deck(LoginRequiredMixin, View):
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

class create_cards(LoginRequiredMixin, View):
    template_name = "flashcards/create_cards.html"

    def get(self, request, deck_id):
        currentDeck = get_object_or_404(Deck, pk=deck_id)
        cards = Card.objects.filter(deck=currentDeck).order_by('-pk')
        return render(request, self.template_name, locals())

    # Notum POST-adferdina i create_deck einnig fyrir create_cards

class edit_card(LoginRequiredMixin, View):
    def post(self, request, card_id=None):
        if card_id != None:
            card = Card.objects.get(id=card_id)
            card.active = False
            card.save()
            return HttpResponse()

        data = request.POST.get("spjald")
        if data:
            spjald = json.loads(data)
            fields = spjald[0]["fields"]
            card = Card.objects.get(id=spjald[0]["pk"])
            if fields["question"]:
                card.question = fields["question"]
            elif fields["answer"]:
                card.answer = fields["answer"]
            elif fields["visible"] != "":
                card.visible = fields["visible"]
            elif fields["active"]:
                card.active = False
            card.save()

        return HttpResponse()
