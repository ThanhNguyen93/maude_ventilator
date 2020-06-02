#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 17:24:10 2020

@author: thanhng
"""


#from lda_in_gensim import *
from lda_in_nltk import *
###read and prepare data
data = pd.read_csv('/Users/thanhng/maude_ventilator/3_building_model/ventilator_subset.csv')



subset = data[(data.brand_name == "['840 VENTILATOR']") | (data.brand_name == "['980 VENTILATOR']")]

subset = subset[subset['text_no_stopword'].notna()].reset_index(drop=True)


#recode abbrevation
replace = subset['text_no_stopword'].copy().tolist()

abbr_dict = {'bd': 'breath delivery',
             'bdu': 'breath delivery unit',
             'cpu': 'central processing unit', 
             'pcb': 'printed circuit board', 
             'fi': 'failure investigation', 
             'cse': 'customer support engineer', 
             'dc': 'direct current', 
             'ui': 'user interface', 
             'se': 'service engineer',
             'gui': 'graphical user interface',
             'tse': 'tech support engineer', 
             'est': 'extended self-testing',
             'pvt': 'performance verification test',
             'sst': 'short self-testing',
             'pt': 'patient', 
             'pvt': 'performance verification test',
             'bennett': 'ventilator', 
             'puritan': 'ventilator', 
             'covidien': 'manufacturer', 
             'device': 'ventilator',
             'nellcor': 'ventilator'
             }

for i in range(len(replace)):    
    for key, val in abbr_dict.items():
        text = replace[i]
        regex_key = r'\b' + key + r'\b'
        regex_val = val
        result = re.search(regex_key, str(text))
        if result:
            replace[i] = re.sub(regex_key, regex_val, text)

subset['replace_abbr'] = replace

###
#in gensim

tokenize, dictionary = TOKENIZE(subset,'replace_abbr')
CHECK_DICTIONARY(dictionary)

bow_corpus = CREATE_BOW_CORPUS(tokenize, dictionary)
CHECK_BOW(20, dictionary,bow_corpus, subset, 'text_lower')



RUN_MODEL(bow_corpus, dictionary, tokenize, 15)


#######
#in nltk
replace = data['replace_abbr']
cv, word_count_vector = COUNTVECTORIZER(replace, 3, 3)

word_count_vector.toarray()

print(cv.get_feature_names())

word_count_vector.inverse_transform()


tfidf_transformer, df_idf = COMPUTE_IDF(cv, word_count_vector)
###lowest idf score means word too common, more docs have this word, less unique



#top unique words with higher idf score


df_idf.tail(20)

df_idf.head(20)

tfidf_df = COMPUTE_TFIDF(cv, tfidf_transformer, replace)

print(tfidf_df.sort_values(by=["tfidf"],ascending=False)[:20])



data_vectorized, word_vectorizer = TFIDF(replace, 3)
PRINT_TFIDF_DF(data_vectorized, word_vectorizer, 20)


lda_model = RUN_LDA(data_vectorized)

PRINT_TOPICS(lda_model, word_vectorizer)



'''
https://stats.stackexchange.com/questions/375062/how-does-topic-coherence-score-in-lda-intuitively-makes-sense

https://www.aclweb.org/anthology/D12-1087.pdf

https://pdfs.semanticscholar.org/1521/8d9c029cbb903ae7c729b2c644c24994c201.pdf
'''

subset.to_csv('ventilator_subset.csv', index=False)
