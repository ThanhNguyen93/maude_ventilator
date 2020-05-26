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





#Create a text column
tokenize = [word.split() for word in data_1['text_tokenize']]
tokenize


'''
Create a dictionary from 'processed_docs' containing the number of times a word appears 
in the whole corpus using gensim.corpora.Dictionary and call it 'dictionary'''

dictionary = gensim.corpora.Dictionary(tokenize)

# Checking dictionary created

count = 0
for k, v in dictionary.iteritems():
    print(k, v)
    count += 1
    if count > 50:
        break


'''
Create the Bag-of-words model for each document 
i.e for each document we create a dictionary reporting how many
words and how many times those words appear. Save this to 'bow_corpus'
'''
bow_corpus = [dictionary.doc2bow(doc) for doc in tokenize]



'''
Preview BOW for our sample preprocessed document
'''
document_num = 25
bow_doc_x = bow_corpus[document_num]
for i in range(len(bow_doc_x)):
    print("Word {} (\"{}\") appears {} time in this document.".format(bow_doc_x[i][0], 
                                                     dictionary[bow_doc_x[i][0]], 
                                                     bow_doc_x[i][1]))


###save corpus into mm format
MmCorpus.serialize('bow_corpus.mm', bow_corpus)
mm = MmCorpus('bow_corpus.mm')
print(mm[1]) #retrieve doc 1



###run LDA


lda_model =  gensim.models.LdaMulticore(corpus = bow_corpus, 
                                   num_topics = 40, 
                                   id2word = dictionary,                                    
                                   workers = 3, 
                                   alpha=0.2, 
                                   eta=0.03)



#measure performance of LDA

from gensim.models.coherencemodel import CoherenceModel



# Compute Coherence Score using c_v
coherence_model_lda = CoherenceModel(model=lda_model, texts=tokenize, dictionary=dictionary, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)

# Compute Coherence Score using UMass
coherence_model_lda = CoherenceModel(model=lda_model, texts=tokenize, dictionary=dictionary, coherence="u_mass")
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)




 
 # Save model to disk.
temp_file = datapath("maude_ventilator_lda_gensim")
lda_model.save(temp_file)


# Load a potentially pretrained model from disk.
lda_model = gensim.models.LdaMulticore.load(temp_file)