from django.db import models

class Deck(models.Model):
    name = models.CharField(max_length=75)

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
