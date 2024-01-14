import collections
import math
import re
import unicodedata
from collections import Counter

import nltk
import six
from bengali_stemmer.rafikamal2014 import RafiStemmer
from idna import unicode
from nltk.corpus import stopwords

from tokenizer import BasicTokenizer

basic_t = BasicTokenizer(False)

en_stemmer = nltk.stem.porter.PorterStemmer()

bn_stemmer = RafiStemmer()

from pyuca import Collator

ck = Collator().sort_key

rfi = open("Dataset/all_word_final.txt", "r", encoding='utf-8')
wfi = open("Dataset/wordNotFound.txt", "w+", encoding='utf-8')

all_words = collections.defaultdict(list)

lines = rfi.readlines()
for line in lines:
    lin = line.split(',')
    en = lin[0].strip().lower()
    bn = lin[1:-1]
    all_words[en] = bn

rfi.close()


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def wordnet_again(source, target, result):
    for wd in source:
        try:
            w = wd.strip().lower()
            if w in result:
                result.append(w)
                continue
            wrd = all_words[w]
            for bn in target:
                strem_wrod = bn_stemmer.stem_word(bn)
                for res in wrd:
                    strem_wrod2 = bn_stemmer.stem_word(res)
                    if ck(strem_wrod) == ck(res):
                        result.append(w)
                        target.remove(bn)
                        break
                    if ck(strem_wrod) == ck(strem_wrod2):
                        result.append(w)
                        target.remove(bn)
                        break
        except:
            wfi.write(w + ',\n')
            print('again', wd)
    # print('secondary', target)
    return result


def wordnet(source, target):
    result = []
    source_en = list(source)
    for wd in source:
        try:
            w = wd.strip().lower()
            if w in result:
                result.append(w)
                source_en.remove(wd)
                continue
            wrd = all_words[w]
            for bn in target:
                for res in wrd:
                    strem_wrod = bn_stemmer.stem_word(res)
                    if ck(bn) == ck(res):
                        result.append(w)
                        target.remove(bn)
                        break
                    if ck(bn) == ck(strem_wrod):
                        result.append(w)
                        target.remove(bn)
                        break
            source_en.remove(wd)
        except:
            try:
                source_en.remove(wd)
            except Exception as e:
                print(e)
            wwd = en_stemmer.stem(wd.strip().lower())
            source_en.append(wwd)
            print('primary Not found', w)
    # print('primary', source_en)
    # print('primary', target)
    result = wordnet_again(source_en, target, result)
    return result


def eng_tokens(text):
    WORD = re.compile(r'\w+')
    words = WORD.findall(text)
    filtered_words = []
    for word in words:
        wrd = str(word).strip().lower()
        if wrd not in stopwords.words('english'):
            filtered_words.append(wrd)

    return filtered_words


def ban_tokens(text):
    bn_tokens = basic_t.tokenize(text)
    return bn_tokens


def text_to_vector(filtered_words):
    # print(filtered_words)
    return Counter(filtered_words)


englishFile = open("Dataset/English1.txt", "r", encoding='utf-8')
banglaFile = open("Dataset/bangla1.txt", "r", encoding='utf-8')
englishFileGogle = open("Dataset/English2.txt", "r", encoding='utf-8')

text1 = englishFile.read()
text2 = banglaFile.read()
txtgoogle = englishFileGogle.read()

english_tokens = eng_tokens(text1)
google_toxens = eng_tokens(txtgoogle)
bangla_tokens = ban_tokens(text2)

print('first', english_tokens)
print('first', bangla_tokens)
result = wordnet(english_tokens, bangla_tokens)
# print(result)
wfi.close()
vector1 = text_to_vector(english_tokens)
vector2 = text_to_vector(google_toxens)
vector3 = text_to_vector(result)

cosine = get_cosine(vector1, vector2)
print('Google translator Cosine:', cosine)
cosine = get_cosine(vector1, vector3)
print('Using wordnet Cosine:', cosine)
