from datetime import date
from supermemo2 import SMTwo
import random
import ast
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Count, Q
from .models import Deck, WordCard, WordLearnHistory
from .utils import *

# Create your views here.

@login_required
def deck_list(request):
    learnt_card_num = WordLearnHistory.objects.filter(
        card__deck__user=request.user, learnt_date=date.today()).count()
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
    first_visit_cards = list(WordCard.objects.filter(deck_id=deck_id, word_learn_history=None).values_list('id', flat=True))
    learnt_cards = list(WordLearnHistory.objects.filter(card__deck_id=deck_id, learnt_date=date.today()).values_list('card_id', flat=True))
    today_review_cards = list(WordLearnHistory.objects.filter(
        card__deck_id=deck_id, next_date=date.today()).exclude(card_id__in=learnt_cards).values_list('card_id', flat=True))
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
        card_id = int(request.POST.get('card_id'))
        time = int(request.POST.get('time')[:-1])
        quality = 1
        feedback = sendAnswerRequest(question, answer)
        correct = (feedback['correct'] == "True") or (feedback['correct'] == 'true')
        if correct:
            quality += 1
            if time > 0:
                quality += 1
                if time >= 10:
                    quality += 1
                    if time >= 20:
                        quality += 1

        review_history = WordLearnHistory.objects.filter(card_id=int(card_id)).order_by('-learnt_date')
        if review_history.count() == 0:
            review = SMTwo.first_review(quality)
            WordLearnHistory.objects.create(card_id=card_id, first_visit=True, easiness=review.easiness, interval=review.interval, next_date=review.review_date).save()
        else:
            last_review = review_history[0]
            print(card_id)
            review = SMTwo(float(last_review.easiness), last_review.interval, 1).review(quality)
            WordLearnHistory.objects.create(card_id=card_id, easiness=review.easiness, interval=review.interval, next_date=review.review_date).save()
        word_dict = WordCard.objects.get(id=card_id).word

        data = {
            'explanation': feedback['explanation'],
            'correct':  json.dumps(correct),
            'word-slug': word_dict.word,
            'word-kanji': word_dict.kanji,
            'word-hiragana': word_dict.hiragana,
            'word-definitions': ' / '.join([word['definition'] for word in ast.literal_eval(word_dict.definitions)])
            }
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest('Invalid request')
    

@login_required
def progress(request):
    date_progress_x = []
    date_progress_y = []
    card_easiness_progress_x = []
    card_easiness_progress_y = []
    
    date_progress = WordLearnHistory.objects.filter(card__deck__user = request.user).values('learnt_date').annotate(Count('card'))
    card_easiness_progress = WordLearnHistory.objects.filter(card__deck__user = request.user).values('easiness').annotate(Count('card'))
    
    for q in date_progress:
        date_progress_x.append(q['learnt_date'].strftime("%d-%m-%Y"))
        date_progress_y.append(q['card__count'])
    for q in card_easiness_progress:
        card_easiness_progress_x.append(q['easiness'])
        card_easiness_progress_y.append(q['card__count'])
    
    data = {
        'date_progress_x': json.dumps(date_progress_x),
        'date_progress_y': json.dumps(date_progress_y),
        'card_easiness_progress_x': json.dumps(card_easiness_progress_x),
        'card_easiness_progress_y': json.dumps(card_easiness_progress_y),
    }
    return render(request, 'decks/progress.html', data)