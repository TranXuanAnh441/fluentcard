from django.db import models
import datetime
from django.conf import settings
from django.db.models import Q
from dictionary.models import WordDict

# Create your models here.
class Deck(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )
    
    @property
    def card_num(self):
        return WordCard.objects.filter(deck=self).count()
    
    @property
    def card_for_review_num(self):
        today_review_cards = WordLearnHistory.objects.filter(
            Q(card__deck=self, next_date=datetime.date.today()) | Q(card__deck=self, learnt_date=datetime.date.today()) 
        ).count()
        cards =  WordCard.objects.filter(deck=self).all()
        learnt_card_list = list(WordLearnHistory.objects.filter(card_id__in=cards).values_list('card_id', flat=True))
        first_visit_cards = len([card.id for card in cards if card.id not in learnt_card_list])
        return first_visit_cards + today_review_cards
    
    @property
    def learnt_card_num(self):
        return WordLearnHistory.objects.filter(card__deck=self, learnt_date=datetime.date.today()).count()

class WordCard(models.Model):
    class CardTypes(models.TextChoices):
        ME = "ME", "meanings"
        KJ = "KJ", "kanji"
        SY = "SY", "synonyms"
        AN = "AN", "antonyms"
        RW = "RW", "related words"
        GM = "GM", "grammars"

    card_type = models.CharField(
        max_length=2,
        choices=CardTypes.choices,
    )
    word = models.ForeignKey(WordDict,on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    
class WordLearnHistory(models.Model):
    card = models.ForeignKey(WordCard,on_delete=models.CASCADE)
    learnt_date = models.DateField(auto_now=True)
    easiness = models.IntegerField(default=1)
    interval = models.IntegerField(default=1)
    next_date = models.DateField(null=True)
    first_visit = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['card', 'learnt_date'], name='unique_card_date_combination'),
        ]