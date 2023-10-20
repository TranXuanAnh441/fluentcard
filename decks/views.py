from django.shortcuts import render, redirect
import random
from datetime import date
from supermemo2 import SMTwo
from .models import Deck, WordCard, WordLearnHistory
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from .utils import *

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
        word_id = int(request.POST['id'])
        WordCard.objects.create(card_type="ME", deck_id=int(deck_id), word_id=word_id).save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def deck_test(request, deck_id):
    cards = WordCard.objects.filter(deck_id=deck_id).all()
    learnt_card_list = list(WordLearnHistory.objects.filter(
        card_id__in=cards).values_list('card_id', flat=True))
    first_visit_cards = [
        card.id for card in cards if card.id not in learnt_card_list]
    today_review_cards = list(WordLearnHistory.objects.filter(
        card_id__in=cards, next_date=date.today()).values_list('card_id', flat=True))
    arr = first_visit_cards + today_review_cards
    if len(arr) == 0:
        redirect('deck_list')
    random.shuffle(arr)
    
    data = {
        'card_ids': json.dumps(arr),
        'question_num': len(arr),
    }
    return render(request, 'decks/deck_test.html', data)


def get_card_question(request):
    if request.method == "POST":
        card_id = request.POST.get('card_id')
        card = WordCard.objects.get(id=int(card_id))
        word_dict = card.word
        question = sendQuestionRequest(word_dict.word)
        data = {
            'question': question,
            'word': word_dict.word,
            'content': word_dict.kanji,
        }
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest('Invalid request')


def get_card_answer(request):
    if request.method == "POST":
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        card_id = request.POST.get('card_id')
        time = int(request.POST.get('time')[:-1])
        quality = 1
        feedback = sendAnswerRequest(question, answer)
        print(feedback)
        correct = (feedback['correct'] == "True") or (feedback['correct'] == 'true')
        if correct:
            quality += 1
            if time > 0:
                quality += 1
                if time >= 10:
                    quality += 1
                    if time >= 20:
                        quality += 1

        review_history = WordLearnHistory.objects.filter(
            card_id=int(card_id)).order_by('-learnt_date')
        if review_history.count() == 0:
            review = SMTwo.first_review(quality)
            WordLearnHistory.objects.create(card_id=int(
                card_id), first_visit=True, easiness=review.easiness, interval=review.interval, next_date=review.review_date).save()
        else:
            last_review = review_history[0]
            review = SMTwo(float(last_review.easiness),
                           last_review.interval, 1).review(quality)
            WordLearnHistory.objects.create(card_id=int(
                card_id), easiness=review.easiness, interval=review.interval, next_date=review.review_date).save()
        card = WordCard.objects.get(id=card_id)

        data = {'explanation': feedback['explanation'],
                'correct':  json.dumps(correct),
                'card-title': card.word.word,
                'card-content': card.word.kanji}
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest('Invalid request')