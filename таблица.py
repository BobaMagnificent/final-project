import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import pandas as pd
from pymorphy2 import MorphAnalyzer
from wiki_ru_wordnet import WikiWordnet
import gensim

def find_syn(word):
    morph = MorphAnalyzer()
    word = morph.parse(word)[0].normal_form
    wikiwordnet = WikiWordnet()
    synsets = wikiwordnet.get_synsets(word)
    synset1 = synsets[0]
    new_list = []
    for w in synset1.get_words():
        new_list.append(w.lemma())
    return new_list[0]


def word_change(string):
    morph = MorphAnalyzer()
    for i in range(len(string)):
        word = morph.parse(string[i])[0]
        grammar_dict = {}
        grammar_dict[i] = [word.tag.POS,
                           word.tag.tense,
                           word.tag.case,
                           word.tag.number,
                           word.tag.gender,
                          ]
        try:
            if grammar_dict[i][0] == 'ADJF':
                new = find_syn(string[i])
                string[i] =  morph.parse(new)[0].inflect({grammar_dict[i][2], grammar_dict[i][3]}).word
            if grammar_dict[i][0] == 'VERB':
                new = find_syn(string[i])
                string[i] =  morph.parse(new)[0].inflect({grammar_dict[i][1], grammar_dict[i][4]}).word
            if grammar_dict[i][0] == 'NOUN':
                new = find_syn(string[i])
                string[i] =  morph.parse(new)[0].inflect({grammar_dict[i][2], grammar_dict[i][3]}).word
        except Exception:
            continue
    string = ' '.join(string)
    string = string.replace(' ,', ',').replace(' .', '.').replace(' !', '!').replace(' ?', '?')
    return string


with open('Борис.txt', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('\n', ' ')
t = sent_tokenize(text)

df = pd.DataFrame()
df['stolbec'] = t


df = df['stolbec'].apply(word_tokenize)


df1 = df.head(601)
df2 = df.tail(100)
df2 = df2.apply(word_change)
print(df2)

df1['answer'] = 1
df2['answer'] = 0
new_df = pd.concat([df1, df2])
new_df1 = new_df.sample(frac=1).reset_index(drop=True)

new_df1.to_csv(r"./dataset.csv", index=True, sep=",")