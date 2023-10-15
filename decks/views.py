from django.shortcuts import render, redirect
from .models import Deck, WordCard, WordLearnHistory
from datetime import date
from django.contrib.auth.decorators import login_required

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