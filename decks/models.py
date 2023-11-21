from django.db import models
from django.conf import settings
from dictionary.models import WordDict
from django.db.models import Q
from datetime import date

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
        arr = list(WordCard.objects.filter(deck=self)
                                    .filter(Q(word_learn_history=None) | 
                                            Q(word_learn_history__next_date=date.today()) | 
                                            Q(word_learn_history__learnt_date=date.today()))
                                    .distinct().values_list('id', flat=True))
        return len(arr)


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
    deck = models.ForeignKey(Deck, related_name='word_card', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    
class WordLearnHistory(models.Model):
    card = models.ForeignKey(WordCard, related_name='word_learn_history', on_delete=models.CASCADE)
    learnt_date = models.DateField(auto_now=True)
    easiness = models.IntegerField(default=1)
    interval = models.IntegerField(default=1)
    next_date = models.DateField(null=True)
    first_visit = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['card', 'learnt_date'], name='unique_card_date_combination'),
        ]