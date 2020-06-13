# Practice
Sample Repository to Practice Coding.


### 1. Computation Linguistics
1a. FST to convert numbers in word form to numeric form (_words_to_number_fst.py_). 
    
    
![Alt text](https://github.com/bharatsesham/Practice/blob/master/media/FST_Words_to_Numbers.png?raw=true "Title")

1b. FST to convert Pinyin words to numbers between 0 and 100 (_pinyin_to_number_fst.pl_).

<img src="https://github.com/bharatsesham/Practice/blob/master/media/FST_Pinyin_to_Numbers.png" align="right">

1c. Eliza Chatbot Example (_basic_eliza_chatbot.py_).

<img src="https://github.com/bharatsesham/Practice/blob/master/media/Eliza_chatbot_example.png" align="middle">

1d. Simple CFG with First Order Logic to parse a sentence (_cfg_sentense_parse.py_). 

    Sentence: "A detective that Sam was arrested by interviewed every male waiter in the bar."
    
_Sample Parse:_
<img src="https://github.com/bharatsesham/Practice/blob/master/media/cfg.png" align="middle">

1e. Generating all available parse trees for a given sentence with a defined grammar (_sentence_parsing.py_). 

_Sample Parses:_
<img src="https://github.com/bharatsesham/Practice/blob/master/media/sentence_parsing.png" align="middle">

Total Parses for the sentence "I put the block in the box on the table in the hallway outside the bedroom near the stairs by the window." are 296. 

### 2. Spark

2a. Spark implementation of Term-Document Frequency to predict Movie Gernes (_termdocumentmatrix.py_). 

2b. Spark implementation of TFIDF to predict Movie Gernes with an increased accuracy (_tfidf.py_). 

2c. Spark implementation of Word2Vec to predict Movie Gernes with best accuracy out of the three methods implemented (_word2vec.py_). 

Sample Preprocessed Data:

<img src="https://github.com/bharatsesham/Practice/blob/master/media/preprocessed_spark_data.png" align="middle">

Sample Processed Data:

<img src="https://github.com/bharatsesham/Practice/blob/master/media/processed_spark_data.png" align="middle">

Sample Output Format:

<img src="https://github.com/bharatsesham/Practice/blob/master/media/sample_spark_output.png" align="left"><br />
<br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />

### 3. Machine Learning

Grid Search
<img src="https://github.com/bharatsesham/Practice/blob/master/media/Grid%20Search.png" align="left">
<br /> <br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />

Confusion Matrix
<img src="https://github.com/bharatsesham/Practice/blob/master/media/Confusion%20Matrix.png" align="left">
<br />
Results on the Dataset:

Accuracy of KNN: 98.779296875<br />
Accuracy of Random Forest: 94.6533203125<br />
Kmeans function has been implemented and the clusters are stored in the variable k_mean_clusters<br />
Dimensions reduced to after applying PCA: 10<br />
WCSS Value: 4187.214989574909<br />
Accuracy of SVM using Scikit:  97.6806640625<br />
Accuracy of Logistic using Scikit:  90.19775390625<br />
Accuracy of Decision Tree using Scikit:  87.51220703125<br />
Accuracy of KNN using Scikit:  98.53515625<br />
Accuracy of the ensembled model using voting classifier in Scikit:  97.27783203125<br />
The sample precision value for logistic regression:  0.902453543374596<br />
The sample recall value for logistic regression: 0.9031051778573826<br />
Time:  1929.2531438300002<br />



