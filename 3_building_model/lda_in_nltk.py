#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 13:36:18 2020

@author: thanhng
"""
import pandas as pd
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
from nltk.corpus import stopwords
from nltk import pos_tag

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD

###tfidf

def COUNTVECTORIZER(data, upper_limit, lower_limit):
    '''count # of words for each doc '''
    cv=CountVectorizer(max_df=0.85, ngram_range=(upper_limit,lower_limit) )
    word_count_vector=cv.fit_transform(data)
    print('# of docs, # of unique words: ', word_count_vector.shape)
    return cv, word_count_vector


def sort_coo(coo_matrix):
    #coo_matrix is word count for a specific doc
    #col is position, .data = # of times a word appear in doc
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def EXTRACT_TOP_COUNTVECTORIZER(coo_matrix, cv):
    index_word = coo_matrix.col
    word_count = coo_matrix.data
    term_doc_df= pd.DataFrame(word_count, index_word).reset_index()
    
    feature_names = cv.get_feature_names()

    term_doc_df['word'] = 'none'
    for (index, count) in zip(term_doc_df.index, term_doc_df[0]):

        term_doc_df.loc[index, 'word']=feature_names[index]       
        term_doc_df.columns=['word_pos_in_corpus', 'word_count_in_this_doc', 'word']

    return term_doc_df.sort_values(by=['word_count_in_this_doc'], ascending=False)[:20]


coo_matrix = word_count_vector[25].tocoo()

EXTRACT_TOP_COUNTVECTORIZER(coo_matrix, cv)



def COMPUTE_IDF(cv, word_count_vector):
    '''compute idf score for the whole corpus'''
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)

 
    # print idf values
    df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names(),columns=["idf_weights"])
     
    # sort ascending
    print(df_idf.sort_values(by=['idf_weights'], ascending=False))
    return tfidf_transformer, df_idf

def COMPUTE_TFIDF(cv, tfidf_transformer, docs):
    # count matrix
    count_vector=cv.transform(docs)
     
    # tf-idf scores tf*idf
    tf_idf_vector=tfidf_transformer.transform(count_vector)
    
    feature_names = cv.get_feature_names()
     
    #get tfidf vector for first document
    first_document_vector=tf_idf_vector[25]
     
    #print the scores
    df = pd.DataFrame(first_document_vector.T.todense(), index=feature_names, columns=["tfidf"])
    print(df.sort_values(by=["tfidf"],ascending=False))
    return df




def TFIDF(data, n_gram):
    word_vectorizer = TfidfVectorizer(
                            stop_words= 'english',
                            sublinear_tf=True,
                            strip_accents='unicode',
                            analyzer='word',
                            token_pattern=r'\w{2,}',  #vectorize 2-character words or more
                            ngram_range=(1, n_gram),
                            use_idf=True)

    data_vectorized = word_vectorizer.fit_transform(data)
    #print('check vocab: ', word_vectorizer.vocabulary_, '\n')
    return data_vectorized, word_vectorizer

def TFIDF_CHECK_PERFORMANCE():
    print('check vocab(key) and their position(items) in dictionary:')
    print(word_vectorizer.vocabulary_.keys())
    print(word_vectorizer.vocabulary_.values()) #position
    print(len(word_vectorizer.get_feature_names())) #dictionary size



def PRINT_TFIDF_DF(data_vectorized, word_vectorizer, index):
    '''return top ifdif score of a doc'''
    df = pd.DataFrame(data_vectorized[index].T.todense(), index=word_vectorizer.get_feature_names(), columns=["tfidf"])
    print(df.sort_values(by=["tfidf"],ascending=False)[:20])


##############

def RUN_LDA(data_vectorized):
    lda_model = LatentDirichletAllocation(n_components=20, max_iter=10, learning_method='online')
    lda_fit= lda_model.fit_transform(data_vectorized)
    print(lda_fit.shape)  # NO_DOCUMENTS, NO_TOPICS)
    return lda_model

def PRINT_TOPICS(model, word_vectorizer, top_n=20):
    for idx, topic in enumerate(model.components_):
        print("\nTopic %d:" % (idx))
        print([(word_vectorizer.get_feature_names()[i], topic[i])
                        for i in topic.argsort()[:-top_n - 1:-1]])


##############
'''
import pyLDAvis.sklearn

import pyLDAvis.gensim

pyLDAvis.enable_notebook()
panel = pyLDAvis.sklearn.prepare(lda_model, data_vectorized, word_vectorizer, mds='tsne')
panel

'''
