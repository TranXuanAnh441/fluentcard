import ast
from datetime import date
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth
from .models import Deck, WordCard, WordLearnHistory
from dictionary.models import WordDict
from .chatGPT_handler import *
from supermemo2 import SMTwo
import random
# Create your views here.


@login_required
def deck_list(request):
    learnt_card_num = WordLearnHistory.objects.filter(
        card__deck__user=request.user, learnt_date=date.today()).count()
    decks = Deck.objects.filter(user=request.user).annotate(
        # card_for_review_num=Count(
        #     'word_card',
        #     distinct=True
        # ),
        learnt_card_num=Count(
            'word_card__word_learn_history',
            filter=Q(word_card__word_learn_history__learnt_date=date.today()),
            distinct=True
        )
    )
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
        WordCard.objects.create(card_type="ME", deck_id=int(
            deck_id), word_id=word_id).save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def deck_test(request, deck_id):
    first_visit_cards = list(WordCard.objects.filter(
        deck_id=deck_id, word_learn_history=None).values_list('id', flat=True))
    learnt_cards = list(WordLearnHistory.objects.filter(
        card__deck_id=deck_id, learnt_date=date.today()).values_list('card_id', flat=True))
    today_review_cards = list(WordLearnHistory.objects.filter(
        card__deck_id=deck_id, next_date=date.today()).exclude(card_id__in=learnt_cards).values_list('card_id', flat=True))
    arr = (list(set(first_visit_cards + today_review_cards)))

    random.shuffle(arr)

    data = {
        'card_ids': json.dumps(arr),
        'question_num': len(arr),
    }
    return render(request, 'decks/deck_test.html', data)


@login_required
def deck_cards(request, deck_id):
    cards = WordDict.objects.filter(wordcard__deck_id=deck_id)
    data = {'cards': cards, 'deck_name': Deck.objects.get(id=deck_id).name }
    return render(request, 'decks/deck_cards.html', data)


def get_card_question(request):
    if request.method == "POST":
        card_id = request.POST.get('card_id')
        if not card_id:
            return redirect('deck_list')
        card = WordCard.objects.get(id=int(card_id))
        word_dict = card.word
        question_data = sendQuestionRequest(word_dict.word)
        if 'options' not in question_data:
            question_data['options'] = 'None'
        else:
            question_data['options'] = json.dumps(question_data['options'])
        data = {
            'question': question_data['question'],
            'options': question_data['options'],
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
        correct = (feedback['correct'] == "True") or (
            feedback['correct'] == 'true')
        if correct:
            quality += 1
            if time > 0:
                quality += 1
                if time >= 15:
                    quality += 1
                    if time >= 30:
                        quality += 1

        review_history = WordLearnHistory.objects.filter(
            card_id=int(card_id)).order_by('-learnt_date')
        if review_history.count() == 0:
            review = SMTwo.first_review(quality)
            WordLearnHistory.objects.create(card_id=card_id, first_visit=True, easiness=review.easiness,
                                            interval=review.interval, next_date=review.review_date).save()
        else:
            last_review = review_history[0]
            review = SMTwo(float(last_review.easiness),
                           last_review.interval, 1).review(quality)
            WordLearnHistory.objects.create(
                card_id=card_id, easiness=review.easiness, interval=review.interval, next_date=review.review_date).save()
        word_dict = WordCard.objects.get(id=card_id).word
        try:
            explanation = feedback['explanation']
        except:
            explanation = feedback['explaination']
        data = {
            'explanation': explanation,
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
    review_progress_x = []
    review_progress_y = []
    card_easiness_progress_x = []
    card_easiness_progress_y = []
    added_card_progress_x = []
    added_card_progress_y = []
    card_interval_x = []
    card_interval_y = []

    # w = WordCard.objects.filter(deck__user=request.user).annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month', 'count')  
    # for t in w:
    #     print(t)

    review_progress = WordLearnHistory.objects.filter(
        card__deck__user=request.user).values('learnt_date').annotate(Count('card'))
    card_easiness_progress = WordLearnHistory.objects.filter(
        card__deck__user=request.user).values('easiness').annotate(Count('card'))
    new_added_card_progress = WordCard.objects.filter(
        deck__user=request.user).values('created_at').annotate(Count('id'))
    card_intervals = WordLearnHistory.objects.filter(
        card__deck__user=request.user).values('interval').annotate(Count('id'))

    for q in review_progress:
        review_progress_x.append(q['learnt_date'].strftime("%d-%m-%Y"))
        review_progress_y.append(q['card__count'])

    for q in card_easiness_progress:
        card_easiness_progress_x.append(q['easiness'])
        card_easiness_progress_y.append(q['card__count'])

    for q in new_added_card_progress:
        added_card_progress_x.append(q['created_at'].strftime("%d-%m-%Y"))
        added_card_progress_y.append(q['id__count'])

    for q in card_intervals:
        card_interval_x.append(str(q['interval']))
        card_interval_y.append(q['id__count'])

    data = {
        'added_average': "{:.2f}".format(sum(added_card_progress_y) / len(added_card_progress_y)),
        'reviewed_average': "{:.2f}".format(sum(review_progress_y) / len(review_progress_y)),
        'easiness_average': "{:.2f}".format(sum(card_easiness_progress_y) / len(card_easiness_progress_y)),
        'review_progress_x': json.dumps(review_progress_x),
        'review_progress_y': json.dumps(review_progress_y),
        'card_easiness_progress_x': json.dumps(card_easiness_progress_x),
        'card_easiness_progress_y': json.dumps(card_easiness_progress_y),
        'added_card_progress_x': json.dumps(added_card_progress_x),
        'added_card_progress_y': json.dumps(added_card_progress_y),
        'card_interval_x': json.dumps(card_interval_x),
        'card_interval_y': json.dumps(card_interval_y),
    }
    return render(request, 'decks/progress.html', data)
