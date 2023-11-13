from django.urls import path
from . import views

urlpatterns = [
    path('prompt_list', views.prompt_list, name='prompt_list'),
    path('chat/<int:prompt_id>', views.chat, name='chat'),
    path('get_chat_response', views.get_chat_response, name='get_chat_response'),
    path('chat_review', views.get_chat_review, name='chat_review'),
    path('add_prompt', views.add_prompt, name='add_prompt'),
]