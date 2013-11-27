from django.db import models
from django.contrib.auth.models import User

class Deck(models.Model):
    name = models.CharField(max_length=75)
    public = models.BooleanField(default=True)
    creator = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class Card(models.Model):
    deck = models.ForeignKey(Deck)
    question = models.CharField(max_length=140)
    answer = models.CharField(max_length=140)

    # asked counts number of times flashcard has appeared
    # wrong counts wrong answers or skips for this question
    asked = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)

    # active denotes whether card is 'deleted' from stack
    # visible denotes whether card is visible
    #         in stack in learning mode (visible in editor)
    active = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.question

# Session logs when a user initiates a new session for a deck
# Needs to be rewritten when we add localstorage functionality.
#class Session(models.Model):
#    user = models.ForeignKey(User)
#    deck = models.ForeignKey(Deck)
#    date = models.DateField(auto_now_add=True)
#    finished = models.DateField(auto_now=True)
#    # active denotes whether the entire deck has been cleared during
#    # this session.
#    active = models.BooleanField(default=True)
#    # index is the index at which the user is currently in the session
#    card = models.ForeignKey(Card)

class Session(models.Model):
    user = models.ForeignKey(User)
    deck = models.ForeignKey(Deck)
    date = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(auto_now=True)

    remaining = models.TextField(default="")
    log = models.TextField(default="")

    active = models.BooleanField(default=True)

#class Answers(models.Model):
#    session = models.ForeignKey(Session)
#    card = models.ForeignKey(Card)
#    right = models.BooleanField(default=True)

class Tag(models.Model):
    name = models.CharField(max_length=75)

    def __unicode__(self):
        return self.name

class AttachTag(models.Model):
    tag = models.ForeignKey(Tag)
    deck = models.ForeignKey(Deck)
