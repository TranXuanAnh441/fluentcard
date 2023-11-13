from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import RoleplayPrompt
from .chatGPT_handler import sendChatMessageRequest, sendChatReviewRequest
from .models import RoleplayPrompt

# Create your views here.

@login_required
def prompt_list(request):
    data = {
        'prompts': RoleplayPrompt.objects.all(),
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
        message = sendChatMessageRequest(msg)
        data = {
            'response': message
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
        image = request.POST['image']
        difficulty = request.POST['difficulty']
        RoleplayPrompt.objects.create(creator=request.user, title=title, description=description, image=image, difficulty=int(difficulty)).save()
    return redirect('prompt_list')