from django.urls import path
from . import views

urlpatterns = [
    path('', views.word_search, name='word_search'),
    path('<str:slug>/details', views.word_detail, name='word_detail'),
]