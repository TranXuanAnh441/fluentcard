import ast
import re
import urllib.parse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from decks.models import Deck, WordCard
from .utils import *
from .models import WordDict, SentenceDict

# Create your views here.

@login_required
def word_search(request):
    search = request.GET.get('search')
    data = {}
    if search:
        data['searchWord'] = search
        words = jisho_word_search(search)
        data['words'] = words
        word_objs = []

        if len(words) > 0:
            if WordDict.objects.filter(word=words[0]['slug']).count() == 0:
                for word in words:
                    word_objs.append(WordDict(word = word['slug'], definitions = str(word['definitions']), hiragana= word['hiragana'], kanji=word['kanji']))
        
        if len(words) > 0:
            WordDict.objects.bulk_create([ obj for obj in word_objs ])
    return render(request, 'dictionary/word_search.html', data)


@login_required
def word_detail(request, slug):
    slug = urllib.parse.unquote(slug)
    id = -1
    try:
        result = WordDict.objects.get(word=slug)
        word = {}
        word['slug'] = result.word
        word['kanji'] = result.kanji
        word['hiragana'] = result.hiragana
        word['definitions'] = ast.literal_eval(result.definitions)
        img = result.image
        id = result.id
        if img == '' or img is None:
            img = get_image(slug)
            result.image = img
            result.save()
    except:
        word = jisho_word_search(slug)[0]
        img = get_image(slug)
        instance = WordDict.objects.create(word = word['slug'], definitions = str(word['definitions']), 
                                hiragana= word['hiragana'], kanji=word['kanji'], image=img).save()
        id = instance.id

    sentences = [sentence for sentence in SentenceDict.objects.filter(word=slug)[:5]]
    if len(sentences) > 0:
        word['sentences'] = [sentence for sentence in sentences]
    else: 
        sentences = jisho_sentence_search(slug)
        word['sentences'] = sentences
        sentence_objs = []
        for sentence in sentences:
            sentence_objs.append(SentenceDict(word=slug, jp_sentence = sentence['jp_sentence'], en_sentence = sentence['en_sentence']))
        if len(sentence_objs) > 0:
            SentenceDict.objects.bulk_create([ obj for obj in sentence_objs ])

    data = {
        'word': word,
        'id': id,
        'word_added': WordCard.objects.filter(word=id).count() > 0,
        'image_url': img,
        'decks': Deck.objects.filter(user=request.user)
    }

    return render(request, 'dictionary/word_detail.html', data)


@login_required
def audio(request):
    if request.method == "POST":
        if request.POST.get('word'):
            data = {
                'src': jisho_word_audio(request.POST.get('word'))
            }
        else:
            sentence = "".join(
                re.split("\(|\)", request.POST.get('sentence').replace(' ', ''))[::2])
            print(sentence)
            data = {
                'src': full_sentence_audio(sentence)
            }
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest('Invalid request')