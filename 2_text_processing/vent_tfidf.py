#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:55:05 2020

@author: thanhng
"""

import nltk
nltk.download(['punkt', 'wordnet'])

import re
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

data = pd.read_csv('~/github_vent_data/ventilator_clean.csv')


#replace vent = ventilator, pt = patient

#data['text_no_stopword'] = data['text_no_stopword'].str.replace('pt', 'patient')


subset = data[(data.brand_name == "['840 VENTILATOR']") | (data.brand_name == "['980 VENTILATOR']")]

subset = subset[subset['text_no_stopword'].notna()]

def display_results(y_test, y_pred):
    labels = np.unique(y_pred)
    confusion_mat = confusion_matrix(y_test, y_pred, labels=labels)
    accuracy = (y_pred == y_test).mean()

    print("Labels:", labels)
    print("Confusion Matrix:\n", confusion_mat)
    print("Accuracy:", accuracy)
    
def LOAD_DATA(data):
    X = data.text_no_stopword.values
    y = data.brand_name.values
    return X, y

def MAIN():   
    X, y = LOAD_DATA(subset)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    
    vect = CountVectorizer(max_df = 0.85)
    tfidf = TfidfTransformer()
    random_forest = RandomForestClassifier()

    # train classifier
    X_train_counts = vect.fit_transform(X_train.tolist())
    X_train_tfidf = tfidf.fit_transform(X_train_counts)
    random_forest.fit(X_train_tfidf, y_train)
    
    # predict on test data
    X_test_counts = vect.transform(X_test)
    X_test_tfidf = tfidf.transform(X_test_counts)
    y_pred = random_forest.predict(X_test_tfidf)
    
    #display result
    display_results(y_test, y_pred)

MAIN()

'''
vect.get_feature_names()
#check # of docs, # of unique words
X_train_counts.shape

#check the top 20 words
print(list(vect.vocabulary_.keys())[:20], '\n')
print('position in sparse vector:', list(vect.vocabulary_.values())[:20])

#count unigram and bigram 

cv=CountVectorizer(max_df=0.85, ngram_range=(1,3))
word_count_vector=cv.fit_transform(X_train.tolist())

cv.get_feature_names()
'''