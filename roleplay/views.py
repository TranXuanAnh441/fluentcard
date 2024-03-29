from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .chatGPT_handler import sendChatMessageRequest, sendChatReviewRequest
from .models import RoleplayPrompt, WordUseHistory
from config.utils import tokenize
from decks.models import WordCard

# Create your views here.

@login_required
def prompt_list(request):
    data = {
        'prompts': RoleplayPrompt.objects.all().order_by('difficulty'),
        'start_num_range': range(1, 4), 
    }
    return render(request, 'roleplay/prompt_list.html', data)


@login_required
def chat(request, prompt_id):
    prompt = RoleplayPrompt.objects.get(id=int(prompt_id))
    first_message = sendChatMessageRequest(prompt.description, first_message=True)
    data = {
        'first_message': first_message,
        'prompt_title': prompt.title,
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    return render(request, 'roleplay/chat.html', data)


def get_chat_response(request):
    if request.method == "POST":
        msg = request.POST.get('message')
        tokens = tokenize(msg)
        response = ''
        word_cards = WordCard.objects.filter(deck__user=request.user).filter(Q(word__word__in=tokens) | Q(word__word__icontains=msg))
        if len(word_cards) > 0 and msg.replace(" ", "") != "":
            response += "From System: "
            for word_card in word_cards:
                WordUseHistory.objects.create(card=word_card).save()
                response += "You used the word: {} in your '{}' deck ! ".format(word_card.word.word, word_card.deck.name)
        message = sendChatMessageRequest(msg)
        data = {
            'system': response,
            'response': message,
        }
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest('Invalid request')


@login_required
def get_chat_review(request):
    message = sendChatReviewRequest()
    data = {
        'review': message
    }
    return render(request, 'roleplay/review.html', data)


@login_required
def add_prompt(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        image_url = request.POST['image']
        if image_url=='':
            image_url = "https://3.bp.blogspot.com/-6pxAA5-dgSg/VPQTsqKsq3I/AAAAAAAAsAs/usDLC-omq9U/s800/zatsudan_woman.png"
        difficulty = request.POST['difficulty']
        RoleplayPrompt.objects.create(creator=request.user, title=title, description=description, image=image_url, difficulty=int(difficulty)).save()
    return redirect('prompt_list')