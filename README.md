## Maude_ventilator

### Topic: 
   exploratory data analysis about ventilator in Maude
### Method: 
   data wrangling in text, NLP
### Tools: 
   scispacy, NLP
   
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
