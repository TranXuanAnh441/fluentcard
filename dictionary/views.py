from django.shortcuts import render
from .utils import *

# Create your views here.
def word_search(request):
    search = (request.GET.get('search'))
    data = {}
    if search:
        data['searchWord'] = search
        words = jisho_word_search(search)
        data['words'] = words
        
    # word_objs = []
    # for word in words:
    #     if WordDict.objects.filter(word=word['slug']).count() == 0 and word['hiragana'] and word['kanji'] and word['definitions']:
    #         word_objs.append(WordDict(word = word['slug'], definitions = str(word['definitions']), hiragana= word['hiragana'], kanji=word['kanji']))
        
    #     if len(words) > 0:
    #         WordDict.objects.bulk_create([ obj for obj in word_objs ])
    return render(request, 'dictionary/word_search.html', data)