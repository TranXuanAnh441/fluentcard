from bs4 import BeautifulSoup, Tag
import requests
import json
import urllib
from jisho_api.word import Word

def jisho_word_search(input):
    data = []
    r = Word.request(input)
    if not r:
        return data
    for d in r.data:
        word = {}
        word['slug'] = d.slug
        word['hiragana'] = d.japanese[0].reading
        kanjis = [j.word for j in d.japanese ]
        word['kanji'] = '/ '.join([str(elem) for elem in kanjis])
        word['definitions'] = []
        for sense in d.senses:
            if 'Wikipedia definition' not in sense.parts_of_speech:
                definition = {}
                definition['definition'] = '; '.join(
                    [str(elem) for elem in sense.english_definitions])
                definition['grammar'] = '; '.join(
                    [str(elem) for elem in sense.parts_of_speech])
                if len(sense.antonyms) > 0:
                    definition['antonyms'] = '; '.join( [str(elem) for elem in sense.antonyms])
                word['definitions'].append(definition)
        data.append(word)
    return data