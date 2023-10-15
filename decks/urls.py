from django.urls import path
from . import views

urlpatterns = [
    path('list', views.deck_list, name='deck_list'),
    path('add', views.add_deck, name='add_deck'),
]