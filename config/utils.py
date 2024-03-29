import requests
import os
import urllib
from bs4 import BeautifulSoup, Tag
from openai import OpenAI
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer


def jisho_word_search(input):
    URL = "https://jisho.org/api/v1/search/words?keyword="
    url = URL + urllib.parse.quote(input)
    r = requests.get(url).json()
    data = []
    if not r:
        return data
    for d in r['data']:
        if any(char.isdigit() for char in d['slug']):
            continue
        word = {}
        word['slug'] = d['slug']
        word['hiragana'] = d['japanese'][0]['reading']
        kanjis = [j['reading'] for j in d['japanese'] ]
        word['kanji'] = '/ '.join([str(elem) for elem in kanjis])
        word['definitions'] = []
        for sense in d['senses']:
            if 'Wikipedia definition' not in sense['parts_of_speech']:
                definition = {}
                definition['definition'] = '; '.join(
                    [str(elem) for elem in sense['english_definitions']])
                definition['grammar'] = '; '.join(
                    [str(elem) for elem in sense['parts_of_speech']])
                if len(sense['antonyms']) > 0:
                    definition['antonyms'] = '; '.join( [str(elem) for elem in sense['antonyms']])
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


def get_image(prompt):
    return image_generation(prompt)


def tokenize(str):
    tokenizer = Tokenizer()
    analyzer = Analyzer(tokenizer=tokenizer)
    # get base form of words
    list_wakati = [token.base_form for token in analyzer.analyze(str)]
    return list_wakati


def image_generation(prompt):
    client = OpenAI(api_key=os.environ.get("CHATGPT"))

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url