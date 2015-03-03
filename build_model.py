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

    def prep_data(self, data):
        "Expects data as list of strings, returns it prepped for self.predict"
        return self.vectorizer.transform(np.array(data))

    def fit(self, X, y):
        X_vect = self.vectorizer.fit_transform(X)
        self.model.fit(X_vect, y)

    def predict(self, X_vect):
        return self.model.predict(X_vect)


def get_data(datafile):
    train = pd.read_csv(datafile)

    X = train['text'].values
    y = train['target'].values

    return X, y


if __name__ == '__main__':
    X, y = get_data('data/train_02032015.csv')
    model = ClassificationModel()
    model.fit(X, y)
    with open('model.pkl', 'w') as f:
        pickle.dump(model, f)