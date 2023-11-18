from django.db import models

# Create your models here.
class Word(models.Model):
    word = models.CharField(max_length=100)
  
    class Meta:
        abstract = True
        
class WordDict(Word):
    definitions = models.CharField(max_length=5000)
    hiragana = models.CharField(max_length=100)
    kanji = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    image = models.URLField(max_length = 1000, null=True) 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['word'], name="word_unique")
        ]

class SentenceDict(Word):
    en_sentence = models.CharField(max_length=1000)
    jp_sentence = models.CharField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)