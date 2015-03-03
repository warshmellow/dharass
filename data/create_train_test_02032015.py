'''
This file details how to create the train test split with file
train_with_target_and_femfreq_mentions_300_02032015.csv.
The above csv has about 450 rows, and two columns: text and target.
The column 'text' holds the text of the tweet, and 'target' holds
1 if contains gendered harassment, 0 otherwise. Note that the first 157
are identified by femfreq herself, while all others are hand classified by
anonymous.

We use sklearn's train_test_split, random state = 1,
and test set size of 20%.

They are written to train_02032015.csv and test_02032015.csv.
'''

import pandas as pd
from sklearn.cross_validation import train_test_split


def main():
    # Set random state and test set size
    RANDOM_STATE = 1
    TEST_SIZE = 0.2

    # Load data
    train_target = pd.read_csv(
        'train_with_target_and_femfreq_mentions_300_02032015.csv')
    X = train_target['text'].values
    y = train_target['target'].values

    # Train/test split and reassemble into DataFrames
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=RANDOM_STATE, test_size=TEST_SIZE)

    train = pd.DataFrame()
    train['text'] = X_train
    train['target'] = y_train

    test = pd.DataFrame()
    test['text'] = X_test
    test['target'] = y_test

    # Write train and test sets to csv
    train.to_csv('train_02032015.csv', index=False, encoding='utf8')
    test.to_csv('test_02032015.csv', index=False, encoding='utf8')


if __name__ == '__main__':
    main()
