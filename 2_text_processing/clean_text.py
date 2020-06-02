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

def NGRAM(text_column):
    uni = UNIGRAM(text_column, 50)
    bigram = BIGRAM(text_column, 50)
    trigram = TRIGRAM(text_column, 50)
    return pd.concat([uni, bigram, trigram], axis = 1)


def EXTRACT_DATA(col, value):
    return data[data[col] == value].reset_index(drop=True)
