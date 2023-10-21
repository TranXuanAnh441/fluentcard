from bs4 import BeautifulSoup, Tag
import requests
import json
import os
import urllib
from jisho_api.word import Word
from bing_image_urls import bing_image_urls

def jisho_word_search(input):
    data = []
    r = Word.request(input)
    if not r:
        return data
    for d in r.data:
        if any(char.isdigit() for char in d.slug):
            continue
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


def jisho_sentence_search(word):
    URL = 'https://jisho.org/search/'
    url = URL + urllib.parse.quote(word + " #sentences")
    url = url.replace(' ', '')
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    res = soup.find_all("div", {"class": "sentence_content"})

    data = []
    for r in res[:5]:
        s1_jp = r.find_all("ul")
        s1_en = r.find_all("span", {"class": "english"})[0].text

        b = ""
        for s in s1_jp:
            for child in s:
                if isinstance(child, Tag):
                    u = child.find("span", {"class": "unlinked"}).text
                    b += u
                    try:
                        f = child.find("span", {"class": "furigana"}).text
                        b += f"({f})"
                    except:
                        pass
                else:
                    b+= child.text
        data.append({"japanese": ''.join(b.split()), "en_translation": s1_en})

    sentences = []
    if data:
        for sentence in data:
            d = {}
            d['jp_sentence'] = sentence['japanese']
            d['en_sentence'] = sentence['en_translation']
            sentences.append(d)
    return sentences


def get_image(word):
    image_urls = bing_image_urls(word, limit=1)
    image_url = ''
    if len(image_urls) > 0:
        image_url = image_urls[0]
    return image_url


def jisho_word_audio(word):
    URL = 'https://jisho.org/word/'
    url = URL + word
    url = url.replace(' ', '')
    r = requests.get(url).content
    soup = BeautifulSoup(r, "html.parser")
    try:
        t = soup.find_all("source", {'type': "audio/mpeg"})[0]
    except:
        return full_sentence_audio(word)
    return t['src']


def full_sentence_audio(sentence):
    url = "https://play.ht/api/v1/convert"

    payload = json.dumps({
        "voice": "ja-JP_EmiV3Voice",
        "content": [
            sentence
        ],
        "title": "japanese sentence pronunciation"
    })

    headers = {
        'Authorization': os.environ.get("AUTHORIZATION"),
        'X-User-ID': os.environ.get("X_USER_ID"),
        'Content-Type': 'application/json'
    }
    response = json.loads(requests.request(
        "POST", url, headers=headers, data=payload).text)
    url = "https://play.ht/api/v1/articleStatus/?transcriptionId=" + \
        response["transcriptionId"]
    headers = {
        "content-type": 'application/json',
        "AUTHORIZATION": os.environ.get("AUTHORIZATION"),
        "X-USER-ID": os.environ.get("X_USER_ID")
    }
    converted = False
    while not converted:
        response = json.loads(requests.get(url, headers=headers).text)
        converted = response['converted']
    return response['audioUrl']