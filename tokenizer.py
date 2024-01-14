import re
import six
import unicodedata
from idna import unicode

import re, math
from collections import Counter
from nltk.corpus import stopwords

stopFile1 = open('stopwordsbn/stopwords_wordnet.txt', 'r', encoding="utf-8")
#stopFile1 = open('stopwordsbn/bn_all_stopword.txt', 'r', encoding="utf-8")



def readStopWords(stopFile):
    stopword = []
    for i in stopFile:
        stopword.append(i.strip())
    return stopword


PUNC_LIST = ["।", "!", "?", ",", ";", "ঃ", "\"", "-", "(", ")", "[", "]"]
stopword = readStopWords(stopFile1)
stopFile1.close()


# removing stopwords from data
def remove_stopwords(tokens):
    token_af_rem_st = []
    for t in tokens:
        if t in PUNC_LIST:
            continue
        if t not in stopword:
            token_af_rem_st.append(t)
    return token_af_rem_st


def convert_to_unicode(text):
    if six.PY3:
        if isinstance(text, str):
            return text
        elif isinstance(text, bytes):
            return text.decode("utf-8", "ignore")
        else:
            raise ValueError("Unsupported string type: %s" % (type(text)))
    elif six.PY2:
        if isinstance(text, str):
            return text.decode("utf-8", "ignore")
        elif isinstance(text, unicode):
            return text
        else:
            raise ValueError("Unsupported string type: %s" % (type(text)))
    else:
        raise ValueError("Not running on Python2 or Python 3?")


def whitespace_tokenize(text):
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    # print("tokens : ", tokens)
    return tokens


def _is_punctuation(char):
    cp = ord(char)
    if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
            (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
        return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
        return True
    return False


class BasicTokenizer(object):

    def __init__(self, do_lower_case=False):
        self.do_lower_case = do_lower_case

    def tokenize(self, text):
        text = convert_to_unicode(text)

        orig_tokens = whitespace_tokenize(text)
        split_tokens = []
        for token in orig_tokens:
            if self.do_lower_case:
                token = token.lower()
                token = self._run_strip_accents(token)
            split_tokens.extend(self._run_split_on_punc(token))

        output_tokens = whitespace_tokenize(" ".join(split_tokens))
        output = remove_stopwords(output_tokens)
        return output

    def _run_strip_accents(self, text):
        text = unicodedata.normalize("NFD", text)
        output = []
        for char in text:
            cat = unicodedata.category(char)
            if cat == "Mn":
                continue
            output.append(char)
        return "".join(output)

    def _run_split_on_punc(self, text):
        chars = list(text)
        i = 0
        start_new_word = True
        output = []
        while i < len(chars):
            char = chars[i]
            if _is_punctuation(char):
                output.append([char])
                start_new_word = True
            else:
                if start_new_word:
                    output.append([])
                start_new_word = False
                output[-1].append(char)
            i += 1
        return ["".join(x) for x in output]
