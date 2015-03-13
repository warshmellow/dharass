'''
Trains and pickles the classifier (model) used for the app.

The one below is a Multinomial Naive Bayes model that takes a the file
train_02032015.csv, and does English stopword removal, only direct
count vectorization.

The classification model expects the tweets to be classified as a list of
strings. It removes screen names before training and predicting.
'''

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.metrics import classification_report
from sklearn.cross_validation import KFold
import cPickle as pickle
import re


class ClassificationModel():
    def __init__(self):
        self.vectorizer = CountVectorizer(stop_words='english')
        self.model = MultinomialNB()

    def fit(self, train_data, train_labels):
        '''
        Takes training data as a list of strings, training labels as
        list of 1 or 0, and fits the model
        '''
        train_data_vectorized = self.vectorizer.fit_transform(train_data)
        self.model.fit(train_data_vectorized, train_labels)

    def predict(self, test_data):
        '''
        Takes test_data which is a list of strings and
        returns a list [(test point, label)]
        '''
        # Preprocess text by removing screen names
        anon_test_data = [re.sub(r'\@\w+', '', text) for text in test_data]
        # Vectorize
        test_data_vectorized = self.vectorizer.transform(anon_test_data)
        # Predict using saved model
        labels = self.model.predict(test_data_vectorized)
        # return list of (data point, label)
        return zip(test_data, labels)


def get_data(datafile):
    train = pd.read_csv(datafile)

    X = train['text'].values
    y = train['target'].values

    return X, y


def load_model(filename):
    'Loads pickle in filename and returns the model'
    with open(filename) as f:
        model = pickle.load(f)
    return model


if __name__ == '__main__':
    # Load training set
    X, y = get_data('data/train_03102015.csv')
    # Anonymize training set by removing screen names
    X = np.vectorize(lambda string: re.sub(r'\@\w+', '', string))(X)
    # Train model
    model = ClassificationModel()
    model.fit(X, y)
    # Save to model.pkl
    with open('model.pkl', 'w') as f:
        pickle.dump(model, f)
