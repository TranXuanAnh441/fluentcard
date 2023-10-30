from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import RoleplayPrompt
from .chatGPT_handler import *
from config.utils import *

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
    # first_message = tokenize(first_message)
    # first_message = 'something something'
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
        # tokens = tokenize(message)
        data = {
            'response': message
        }
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest('Invalid request')