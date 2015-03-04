'''
Trains and pickles the classifier (model) used for the app.

The one below is a Bernoulli Naive Bayes model that takes a the file
train_02032015.csv, and does NO text preprocessing, only direct
binary count vectorization.

The classification model expects the tweets to be classified as a list of
strings.
'''

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import classification_report
from sklearn.cross_validation import KFold
import cPickle as pickle


class ClassificationModel():
    def __init__(self):
        self.vectorizer = CountVectorizer(binary=True)
        self.model = BernoulliNB()

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
        # Preprocess text if needed
        # Vectorize
        test_data_vectorized = self.vectorizer.transform(test_data)
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
    X, y = get_data('data/train_02032015.csv')
    model = ClassificationModel()
    model.fit(X, y)
    with open('model.pkl', 'w') as f:
        pickle.dump(model, f)
