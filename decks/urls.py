from django.urls import path
from . import views

urlpatterns = [
    path('list', views.deck_list, name='deck_list'),
    path('add_deck', views.add_deck, name='add_deck'),
    path('add_card', views.add_card, name='add_card'),
]