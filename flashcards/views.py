from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone
from django.core import serializers
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from flashcards.models import *
import json
from braces.views import LoginRequiredMixin
from django.utils.html import escape

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
        decks_created_by_current_user = Deck.objects.filter(creator=request.user)
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

    # This method is used to create both Deck entries and Card entries
    def post(self, request):
        objects = []
        # If the posted item is a stack and not a card
        if request.POST.get("stafli"):
            print("here")
            data = json.loads(request.POST.get("stafli"))[0]
            print(data)
            # Escape HTML-elements from our strings
            # (Not strictly necessary)
            data['fields']['creator'] = User.objects.get(pk=request.user.pk)
            data['fields']['name'] = escape(data['fields']['name'])
            deck = Deck(**data['fields'])
            deck.save()
            pk = str(deck.pk)
            url_to_deck = "/create/" + pk + "/"
            return HttpResponseRedirect(url_to_deck)
        # If the posted item is a card and not a stack
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
        # Check whether current user created the requested stack
        if request.user == currentDeck.creator:
            print("typpo")
            cards = Card.objects.filter(deck=currentDeck).order_by('-pk')
            return render(request, self.template_name, locals())
        # If not, we tell the off (Change later)
        return HttpResponse("Skamm!")

    # We use the POST-method from create_deck to create cards

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
