from django.urls import path
from . import views

urlpatterns = [
    path('list', views.deck_list, name='deck_list'),
    path('<int:deck_id>/cards', views.deck_cards, name='deck_cards'),
    path('add_deck', views.add_deck, name='add_deck'),
    path('add_card', views.add_card, name='add_card'),
    path('<int:deck_id>/deck_test', views.deck_test, name='deck_test'),
    path('get_card_question', views.get_card_question, name='get_card_question'),
    path('get_card_answer', views.get_card_answer, name='get_card_answer'),
    path('progress', views.progress, name='progress'),
]