from django.shortcuts import render

# Create your views here.
def word_search(request):
    return render(request, 'dictionary/word_search.html')