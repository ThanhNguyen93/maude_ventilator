#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 13:01:57 2020

@author: thanhng
"""
import pandas as pd
import numpy as np
import re
import spacy
from spacy.lang.en import English
from datetime import datetime

import nltk
import time


nlp = spacy.load("en_core_sci_sm")


data = pd.read_csv('ventilator_clean.csv')

data_1['event_type'].value_counts()

data_1 = data.dropna(subset=['event_type'])

data.isna().sum()

data['event_type']


#combine text column
data['text'] = data['event_description'] + ' ' + data['manufacturer_narrative']
data['text_clean'] = data['text'].copy()
#lower case
data['text_clean'] = data['text_clean'].str.lower()



######clean text

def LEMMATIZER(doc):
    doc = [token.lemma_ for token in doc if token.lemma_ != '-PRON-']
    doc = u' '.join(doc)
    return nlp.make_doc(doc)

def REMOVE_STOPWORDS(doc):
    doc = [token.text for token in doc if token.is_stop != True]
    doc = u' '.join(doc)
    return nlp.make_doc(doc)

def REMOVE_PUNCT(doc):
    doc = [token for token in doc if not token.is_punct]
    doc = ', '.join(str(word) for word in doc if str(word).isalnum())
    return doc

def GET_UNIQUE_WORD(doc):
    return ', '.join(word for word in set(doc.split(' ')))


nlp.add_pipe(LEMMATIZER,name='lemmatizer',after='ner')
#nlp.add_pipe(REMOVE_STOPWORDS, name="stopwords", after='lemmatizer')
nlp.add_pipe(REMOVE_PUNCT, name="punctuation", last= True)

print(nlp.pipe_names)



#convert text column to list to feed to nlp pipeline
lst_text = data['text_lower'].tolist()



#keep stopword
text_col = []
for doc in nlp.pipe(lst_text, n_threads=3):
    text_col.append(doc)

text_col[0]

data['text_has_stopword'] = text_col

data['text_has_stopword'] = data['text_has_stopword'].replace('pt', 'patient')

data['text_has_stopword'] = data['text_has_stopword'].replace(' none', ' ')





data.to_csv('ventilator_clean.csv', index = False)


#tokenize & remove stopword
def TOKENIZE_RM_STOPWORD(word_lst):
    tokenize = nltk.word_tokenize(str(word_lst))

    punct=["[", "]", ",", "'", "none", "...", ":"]
    return[token for token in tokenize if token not in punct]


#unigram
def UNIGRAM(word_lst, N):
    tokenize_lst = TOKENIZE_RM_STOPWORD(word_lst)
    unigram = nltk.FreqDist(tokenize_lst).most_common(N)
    return pd.DataFrame(unigram,columns=['Unigram', 'Unigram_Frequency'])

#bigrams
def BIGRAM(word_lst, N):
    tokenize_lst = TOKENIZE_RM_STOPWORD(word_lst)
    bigram = nltk.FreqDist(list(nltk.bigrams(tokenize_lst))).most_common(N)
    return pd.DataFrame(bigram,columns=['Bigram', 'Bigram_Frequency'])

#trigrams
def TRIGRAM(word_lst, N):
    tokenize_lst = TOKENIZE_RM_STOPWORD(word_lst)
    trigram = nltk.FreqDist(list(nltk.trigrams(tokenize_lst))).most_common(N)
    return pd.DataFrame(trigram,columns=['Trigram', 'Trigram_Frequency'])






#rename text_tokenize to text_remove_stopword, comma sep

text_column = data['text_has_stopword'].tolist()


def NGRAM(text_column):
    uni = UNIGRAM(text_column, 50)
    bigram = BIGRAM(text_column, 50)
    trigram = TRIGRAM(text_column, 50)
    return pd.concat([uni, bigram, trigram], axis = 1)

start = time.time()
ngram_df = NGRAM(text_column)
print(time.time() - start)

ngram_df.to_csv('vent_ngram.csv', index=False)

#extract event_type

def EXTRACT_DATA(col, value):
    return data[data[col] == value].reset_index(drop=True)





malfunction = EXTRACT_DATA('event_type', "Malfunction")
injury =EXTRACT_DATA('event_type', "Injury")
death = EXTRACT_DATA('event_type', "Death")


malf_text = malfunction['text_has_stopword'].tolist()
malfunction_ngram = NGRAM(malf_text)


death_text = death['text_has_stopword'].tolist()
death_ngram = NGRAM(death_text)

injury_text = injury['text_has_stopword'].tolist()
injury_ngram=NGRAM(injury_text)


malfunction_ngram.to_csv('vent_malf_ngram.csv', index=False)

death_ngram.to_csv('vent_death_ngram.csv', index=False)

injury_ngram.to_csv('vent_injury_ngram.csv', index=False)



###extract data based on devices

V890 = EXTRACT_DATA('brand_name', "['V890']")

V899 = EXTRACT_DATA('brand_name', "['V890']")

for device in devices_interested:
    print(NGRAM(device, 'text_has_stopword'), '\n')












#get unique word for each row

start=datetime.now()

data['text_unique_word'] = 'none'

for index in range(data.shape[0]):
    text = data['text_tokenize'][index]
    data.loc[index, 'text_unique_word'] =  GET_UNIQUE_WORD(text)



print (datetime.now()-start)


data[data['text_unique_word'] == 'none']

data['text_unique_word']

data.to_csv('ventilator_clean.csv', index = False)
