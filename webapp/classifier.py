import os
import string
import numpy as np
import sys
from sklearn import datasets
import DataPrepare
import nltk
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pickle

data_path = 'data' # the directory for storing the extracted files
data_prepare = DataPrepare.DataPrepare()
train_path, test_path = data_prepare.extract('data.tgz', data_path)
target_path = 'data/data/train_subsample'
subsample_path = data_prepare.subsample(train_path, target_path)

train_data = datasets.load_files(subsample_path, encoding='latin-1')
test_data = datasets.load_files(test_path, encoding='latin-1')

wnl = nltk.wordnet.WordNetLemmatizer()
stop_words = ENGLISH_STOP_WORDS
analyzer = CountVectorizer().build_analyzer()

def penn2morphy(penntag):
    """ Converts Penn Treebank tags to WordNet. """
    morphy_tag = {'NN':'n', 'JJ':'a','VB':'v', 'RB':'r'}
    try:
        return morphy_tag[penntag[:2]]
    except:
        return 'n'

def lemmatize_sent(list_word):
    # Text input is string, returns array of lowercased strings(words).
    return [wnl.lemmatize(word.lower(), pos=penn2morphy(tag)) 
            for word, tag in pos_tag(list_word)]

def lemmatize_rmv_nums(doc):
    #To remove terms that are numbers(e.g. "123", "-45", "6.7" etc.)
    return (word for word in lemmatize_sent(analyzer(doc)) if word not in stop_words and not word.isdigit())

# Stopwords remove
analyzer = CountVectorizer().build_analyzer()
# vectorizer = CountVectorizer(min_df = 3, analyzer = lemmatize_rmv_nums, stop_words = 'english')
vectorizer = CountVectorizer(min_df = 3, stop_words = 'english')

X_train = vectorizer.fit_transform(train_data.data)
pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))
X_test = vectorizer.transform(test_data.data)

# Perform TF-IDF transformation
tfidf_T = TfidfTransformer()

X_train_tfidf = tfidf_T.fit_transform(X_train)# TF-IDF matrix of the train dataset
pickle.dump(tfidf_T, open('tfidf.pkl', 'wb'))
X_test_tfidf = tfidf_T.transform(X_test)# TF-IDF matrix of the test dataset

y_train = train_data.target
y_test = test_data.target

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

classification = MultinomialNB()
classification.fit(X_train_tfidf, y_train)
pickle.dump(classification, open('model.pkl', 'wb'))

y_train_pred = classification.predict(X_train_tfidf)
print('Training Score: ', classification.score(X_train_tfidf, y_train))
print(classification_report(y_train, y_train_pred, target_names=train_data.target_names))


y_pred = classification.predict(X_test_tfidf)
print('Testing Score: ', classification.score(X_test_tfidf, y_test))
print(classification_report(y_test, y_pred, target_names=test_data.target_names))
