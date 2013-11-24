from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone
from django.core import serializers
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from flashcards.models import *
from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
import json

class view_decks(LoginRequiredMixin, View):
    template_name = "flashcards/view_decks.html"
    
    def get(self, request):
        decks = Deck.objects.all()
        user = request.user
        decks_created_by_current_user = Deck.objects.filter(creator=request.user)
        return render(request, self.template_name, locals())

class deck(LoginRequiredMixin, View):
    template_name = "flashcards/view_single_deck.html"

    # Creates a new session for the current user for deck_id,
    # starting from the first card in the deck
    def createSession(self, deck, cards):
        current = cards[:1].get()
        session = Session(**{'user': self.request.user, 'deck': deck, 'card': current})
        session.save()
        return session

    def get(self, request, deck_id):
        decks = Deck.objects.all()
        user = request.user
        decks_created_by_current_user = Deck.objects.filter(creator=user)
        deck = Deck.objects.get(pk=deck_id)
        
        # We check whether there is an active Session for this user and deck,
        # and if so, we load the corresponding cards. That is, the user is not
        # given cards they have already answered in this session.
        try:
            session = Session.objects.get(user=request.user, deck=deck_id, active=True)
            current = session.card.pk
            cards = Card.objects.filter(deck=deck_id, pk__gt=current)
            
            # Safety valve, if for some reason cards has been cleared, but
            # session not set to active=False
            if not cards:
                session.active = False
                cards = Card.objects.filter(deck=deck_id)
                session = self.createSession(deck, cards)
        # If not, we create a new Session
        except Session.DoesNotExist:
            cards = Card.objects.filter(deck=deck_id)
            try:
                session = self.createSession(deck, cards)
            # If current stack is empty:
            except Card.DoesNotExist:
                return HttpResponse("Bjakk!")

        except Session.MultipleObjectsReturned:
            sessions = Session.objects.filter(user=request.user, deck=deck_id, active=True)
            for s in sessions:
                answers = Answers.objects.filter(session=s)
                if not answers:
                    s.delete()
                else:
                    s.active = False
                    s.save()
            cards = Card.objects.filter(deck=deck_id)
            session = self.createSession(deck, cards)

        creator = False
        if request.user == deck.creator:
            creator = True
        session_id = session.pk
        return render(request, self.template_name, locals())

    # This function receives an AJAX POST and updates the session and answer
    # ratio of the card.
    # A touch of security through obscurity here.
    # Ugly hack, fix later.
    def post(self, request, card_id, session_id, is_last):
        session = Session.objects.get(pk=session_id)
        if request.user != session.user or not session.active:
            return HttpResponse("Skamm!")
        card = Card.objects.get(pk=card_id)
        card.asked += 1
        
        try:
            answer = Answers.objects.get(session=session, card=card)
            not_answered = False
        except Answers.DoesNotExist:
            answer = Answers(**{'session': session, 'card': card})
            not_answered = True
            session.card = card

        ans = request.POST.get("svar")
        if ans == "rangt":
            if not_answered:
                answer.right = False
            card.wrong +=1
        if not_answered:
            answer.save()
        card.save()

        if is_last == '1':
            session.active = False
        session.save()
        return HttpResponse()

class create_deck(LoginRequiredMixin, View):
    template_name = "flashcards/create_deck.html"
    def get(self, request):
        decks = Deck.objects.all()
        user = request.user
        decks_created_by_current_user = Deck.objects.filter(creator=user)
        return render(request, self.template_name, locals())

    # This method is used to create both Deck entries and Card entries
    def post(self, request):
        objects = []
        # If the posted item is a stack and not a card
        if request.POST.get("stafli"):
            data = json.loads(request.POST.get("stafli"))[0]
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
        decks = Deck.objects.all()
        user = request.user
        currentDeck = get_object_or_404(Deck, pk=deck_id)
        decks_created_by_current_user = Deck.objects.filter(creator=user)
        # Check whether current user created the requested stack
        if request.user == currentDeck.creator:
            cards = Card.objects.filter(deck=currentDeck).order_by('-pk')
            return render(request, self.template_name, locals())
        # If not, we tell them off (Change later)
        return HttpResponse("Skamm!")

    # We use the POST-method from create_deck to create cards

# Toggles the public-status of a deck, if and only if
# the user who created the deck calls it.
@login_required
def togglePublic(request, deck_id, public_status):
    deck = Deck.objects.get(pk=deck_id)
    if deck.creator == request.user:
        if public_status == '0':
            deck.public = False
        else:
            deck.public = True
        print(deck.public)
        deck.save()
        return HttpResponse()
    else:
        return HttpResponse()

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
