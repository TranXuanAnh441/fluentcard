from django.conf import settings
from django.db import models
from decks.models import WordCard

# Create your models here.
class RoleplayPrompt(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )
    description = models.CharField(max_length=700)
    difficulty = models.IntegerField(default=1)
    image = models.URLField(max_length = 1000, null=True)

class WordUseHistory(models.Model):
    card = models.ForeignKey(WordCard, related_name='word_use_history', on_delete=models.CASCADE)
    learnt_date = models.DateTimeField(auto_now=True)