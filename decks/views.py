from django.shortcuts import render, redirect
from .models import Deck, WordCard, WordLearnHistory
from datetime import date
from django.contrib.auth.decorators import login_required
import ast

# Create your views here.

@login_required
def deck_list(request):
    learnt_card_num = WordLearnHistory.objects.filter(
        learnt_date=date.today()).count()
    decks = Deck.objects.filter(user=request.user)
    data = {
        'decks': decks,
        'learnt_card_num': learnt_card_num,
    }
    return render(request, 'decks/deck_list.html', data)


@login_required
def add_deck(request):
    if request.method == "POST":
        deck_name = request.POST['deck_name']
        Deck.objects.create(user=request.user, name=deck_name).save()
    return redirect('deck_list')


@login_required
def add_card(request):
    if request.method == "POST":
        deck_id = int(request.POST['deck_id'])
        slug = request.POST['slug']
        meanings = request.POST['definitions']
        kanji = request.POST['kanji']
        definitions = []

        for meaning in ast.literal_eval(meanings):
            definitions.append(meaning['definition'] +  f" {meaning['grammar']}")
        WordCard.objects.create(card_type="ME", word=slug, deck_id=int(
            deck_id), content=str(definitions)).save()

    return redirect(request.META.get('HTTP_REFERER'))