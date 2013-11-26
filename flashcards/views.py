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
    def createSession(self, deck):
        cards = Card.objects.filter(deck=deck)
        if cards:
            card_ids = json.dumps(json.dumps([c.pk for c in cards]))
            session = Session(**{'user': self.request.user, 'deck': deck, 'remaining': card_ids})
            session.save()
            return session
        # If the stack is empty we don't create a new session
        return None

    def get(self, request, deck_id):
        user = request.user
        decks_created_by_current_user = Deck.objects.filter(creator=user)
        deck = Deck.objects.get(pk=deck_id)
        
        # We check whether there is an active Session for this user and deck,
        # and if so, we load the corresponding cards. That is, the user is not
        # given cards they have already answered in this session.
        try:
            session = Session.objects.get(user=request.user, deck=deck_id, active=True)
        # If not, we create a new Session
        except Session.DoesNotExist:
            session = self.createSession(deck)

        # A bit of a dirty hack, should be rectified once session system is
        # rewritten
        except Session.MultipleObjectsReturned:
            session = None
            sessions = Session.objects.filter(user=request.user, deck=deck_id, active=True)
            for s in sessions:
                if s.log == None:
                    s.delete()
                else:
                    session = s
                    break
            if not session:
                session = self.createSession(deck)

        creator = False
        if request.user == deck.creator:
            creator = True

        session_id = None
        answered = None
        if session != None:
            session_id = session.pk
            res = []
            remaining = json.loads(json.loads(session.remaining))
            for r in remaining:
                res.append(r)
            cards = Card.objects.filter(pk__in=res)


        return render(request, self.template_name, locals())

    # This function receives an AJAX POST and updates the session and answer
    # ratio of the card.
    def post(self, request, card_id, session_id):
        session = Session.objects.get(pk=session_id)
        if (request.user != session.user) or (session.remaining == None):
            return HttpResponse("Skamm!")
        card = Card.objects.get(pk=card_id)
        card.asked += 1
        ans = request.POST.get("svar")
        remaining = request.POST.get("remaining")

        res = {card_id: (ans == "rett")}
        if not session.log:
            session.log = json.dumps([res])
        else:
            svor = json.loads(session.log)
            svor.append(res)
            session.log = json.dumps(svor)
   
        if ans == "rangt":
            card.wrong +=1
            
        card.save()
        session.remaining = json.dumps(remaining)

        if session.remaining == "\"[]\"":
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
            data['fields']['name'] = escape(data['fields']['name'])[:75]
            deck = Deck(**data['fields'])
            deck.save()
            pk = str(deck.pk)
            url_to_deck = "/create/" + pk + "/"
            return HttpResponseRedirect(url_to_deck)
        # If the posted item is a card and not a stack
        elif request.POST.get("spjald"):
            for o in serializers.deserialize("json", request.POST.get("spjald")):
                if (o.object.question and o.object.answer):
                    o.object.question = o.object.question[:140]
                    o.object.answer = o.object.answer[:140]
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
