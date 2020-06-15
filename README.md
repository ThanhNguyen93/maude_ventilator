## Maude_ventilator

**Topic:** exploratory data analysis about ventilators in Maude

**Method:** data wrangling in text, NLP

**Tools:** scispacy, NLP

**Data source:** https://open.fda.gov/apis/device/event/
   
<hr />

**Background:** In the surge of covid and shortage of ventilators, many companies try to make their own ventilator machines. The purpose of this project is to investigate adverse events caused by ventilators using FDA medical device adverse event database. More specific, this project only focused on Medtronic Puritan Bennett™ 980 and 840 Ventilator and analyzed what are the main problems with these two series. 


**Objectives:** 
- What are the main problems with these 2 models? 
- Model 980 is an update version of 840 with many new improvement features. By applying LDA, I want to check if the well-known problems in 840 model still exist in the new model 980
- Apply unigram, bigram and trigram LDA and compare their performance on these texts

https://hcpresources.medtronic.com/blog/make-the-comparison-the-puritan-bennett-840-versus-the-puritan-bennett-980-ventilators


<hr />

### [Data collection](https://github.com/ThanhNguyen93/maude_ventilator/tree/master/1_data_collection)
- [x] collect data using MAUDE API

### NLP pipeline
#### 1. [Text processing](https://github.com/ThanhNguyen93/maude_ventilator/tree/master/2_text_processing)
- [x] using Scispacy, cleaning, normalization, tokenization, stopword removal, POS tagging, stemming and lemmatization

#### 2. Feature extraction
- [x] 1. Frequency-based: count vector, tf-idf, co-occurence
- [ ] 2. Prediction-based on probability: word2vec (CBOW, skipgram)
  
#### 3. [Buidling models](https://github.com/ThanhNguyen93/maude_ventilator/tree/master/3_building_model)
- [x] Topic modeling using LDA, measure performance by coherence score
