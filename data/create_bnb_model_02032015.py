'''
Creates and prints classification report on a baseline model that has
been trained on train_02032015.csv and validated on test_02032015.csv.

The baseline model is a Bernoulli Naive Bayes model with Binary vectorization
of text and, most importantly, verbatim text of tweets. Again, that's NO
cleaning of the text.

The cross validated precision, recall, f1-score, and support are as follows:
precision    recall  f1-score   support
1       0.82      0.93      0.87        30
1       0.90      0.87      0.88        30
1       0.73      0.89      0.80        27
1       0.77      0.88      0.82        34
1       0.76      0.94      0.84        31

The test set such scores are:
1       0.76      0.96      0.85        27

They are generated below.
'''

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import classification_report
from sklearn.cross_validation import KFold


def main():
    # Define number of folds, random states
    N_FOLDS = 5
    RANDOM_STATE = 1

    # Read in training and test data
    train = pd.read_csv('train_02032015.csv')
    test = pd.read_csv('test_02032015.csv')

    X = train['text'].values
    y = train['target'].values

    # Train models under Cross Validation and print classification report
    kf = KFold(
        len(X), n_folds=N_FOLDS, shuffle=True, random_state=RANDOM_STATE)

    for train_index, test_index in kf:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        count_vect = CountVectorizer(binary=True)
        X_train_bin = count_vect.fit_transform(X_train)
        X_test_bin = count_vect.transform(X_test)

        bnb_model = BernoulliNB()
        bnb_model.fit(X_train_bin, y_train)
        y_test_pred = bnb_model.predict(X_test_bin)

        print "Classification Report for CV Fold"
        print classification_report(y_test, y_test_pred)

    # Train model on whole training set and print classification report
    # on test set.
    X_test_real = test['text'].values
    y_test_real = test['target'].values

    X_bin = count_vect.fit_transform(X)
    X_test_real_bin = count_vect.transform(X_test_real)

    bnb_model.fit(X_bin, y)
    y_pred_test_real = bnb_model.predict(X_test_real_bin)

    print "Classification Report on Test Set"
    print classification_report(y_test_real, y_pred_test_real)


if __name__ == '__main__':
    main()
