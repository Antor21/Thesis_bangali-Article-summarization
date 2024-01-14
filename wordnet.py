import collections

from pyuca import Collator

ck = Collator().sort_key

rfi = open("Dataset/all_en_bn.txt", "r", encoding='utf-8')
all_words = collections.defaultdict(list)

lines = rfi.readlines()
for line in lines:
    lin = line.split(',')
    en = lin[0].strip().lower()
    bn = lin[1:-1]
    all_words[en] = bn

rfi.close()

source = ['I', 'eat', 'rice', 'goes', 'market', 'he', 'really', 'good' 'man']
target = ['আমি', 'ভাত', 'খাই']
result=[]

def wordnet():
    for wd in source:
        try:
            w = wd.strip().lower()
            if w in result:
                continue
            wrd = all_words[w]
            for bn in target:
                for res in wrd:
                    if ck(bn) == ck(res):
                        result.append(w)
                        target.remove(bn)
        except:
            print(wd)
    return result
print(target)
print(wordnet())