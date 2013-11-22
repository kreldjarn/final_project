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
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=300)

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
class Session(models.Model):
    user = models.ForeignKey(User)
    deck = models.ForeignKey(Deck)
    date = models.DateField(auto_now=True)

# Answers logs the answers of each session
class Answers(models.Model):
    session = models.ForeignKey(Session)
    card = models.ForeignKey(Card)
    right = models.BooleanField(default=True)

class Tag(models.Model):
    name = models.CharField(max_length=75)

    def __unicode__(self):
        return self.name

class AttachTag(models.Model):
    tag = models.ForeignKey(Tag)
    deck = models.ForeignKey(Deck)
