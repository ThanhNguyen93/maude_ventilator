
import numpy as np
import pandas as pd
import spacy, re, nltk

import gensim, logging, warnings
import gensim.corpora as corpora
from gensim.utils import lemmatize, simple_preprocess
from gensim.models import CoherenceModel

from gensim.corpora import MmCorpus
from gensim.test.utils import get_tmpfile
from gensim.test.utils import datapath

 from gensim.models.phrases import Phrases, Phraser

from sklearn.model_selection import GridSearchCV



def TOKENIZE(data, col):
    tokenize = [word.split() for word in data[col]]
    '''
    Create a dictionary from 'processed_docs' containing the number of times a word appears 
    in the whole corpus using gensim.corpora.Dictionary and call it 'dictionary'''
    
    dictionary = gensim.corpora.Dictionary(tokenize)
    return tokenize, dictionary


def CHECK_DICTIONARY(dictionary):
    # Checking dictionary created
    count = 0
    for k, v in dictionary.iteritems():
        print(k, v)
        count += 1
        if count > 50:
            break

def CREATE_BOW_CORPUS(tokenize, dictionary):
    '''
    Create the Bag-of-words model for each document 
    i.e for each document we create a dictionary reporting how many
    words and how many times those words appear. Save this to 'bow_corpus'
    '''
    bow_corpus = [dictionary.doc2bow(doc) for doc in tokenize]
    return bow_corpus


def CHECK_BOW(document_num, dictionary, bow_corpus, data, ori_col):
    '''
    Preview BOW for our sample preprocessed document
    '''
    print('original text: ', data[ori_col][document_num], '\n')
    bow_doc_x = bow_corpus[document_num]
    for i in range(len(bow_doc_x)):
        print("Word {} (\"{}\") appears {} time in this document.".format(bow_doc_x[i][0], 
                                                         dictionary[bow_doc_x[i][0]], 
                                                         bow_doc_x[i][1]))


def SAVE_CORPUS_MM_FORMAT():
    ###save corpus into mm format
    MmCorpus.serialize('bow_corpus.mm', bow_corpus)
    mm = MmCorpus('bow_corpus.mm')
    print(mm[1]) #retrieve doc 1



###run LDA
###high eta  = topic has more word
### high alpha = more topic

def RUN_LDA(bow_corpus, dictionary):
    lda_model =  gensim.models.LdaMulticore(corpus = bow_corpus, 
                                       num_topics = 30, 
                                       id2word = dictionary,                                    
                                       workers = 3, 
                                       alpha=0.1, 
                                       eta=0.02)
    return lda_model

    

def LDA_PERFORMANCE(lda_model, tokenize, dictionary):
    # Compute Coherence Score using c_v
    coherence_model_lda = CoherenceModel(model=lda_model, texts=tokenize, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score using c_v: ', coherence_lda)
    
    # Compute Coherence Score using UMass
    coherence_model_lda = CoherenceModel(model=lda_model, texts=tokenize, dictionary=dictionary, coherence="u_mass")
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score using UMass: ', coherence_lda)
    

def PRINT_TOPIC(lda_model, num_topics):
    for idx,topic in lda_model.show_topics(formatted=True, num_topics=num_topics, num_words=25):
        print("Topic: {} \nWords: {}".format(idx, topic ))
        print("\n")
        

def RUN_MODEL(bow_corpus, dictionary, tokenize, num_topics):
    lda_model = RUN_LDA(bow_corpus, dictionary)
    print('\nLDA PERFORMANCE:')
    LDA_PERFORMANCE(lda_model, tokenize, dictionary)
    print('\nPRINT TOPICS:')
    PRINT_TOPIC(lda_model, num_topics)











'''    
###gridsearchCV

parameters = {'num_topic': [15, 20, 30, 40], \
                'alpha': [0.1, 0.2, 0.3], \
                'eta':[0.03, 0.04, 0.05, 0.06]}    

# Init Grid Search Class
gridsearch = GridSearchCV(lda_model, param_grid=parameters)

# Do the Grid Search
gridsearch.fit(bow_corpus)
    


 # Save model to disk.
temp_file = datapath("maude_ventilator_lda_gensim")
lda_model.save(temp_file)


# Load a potentially pretrained model from disk.
lda_model = gensim.models.LdaMulticore.load(temp_file)

'''