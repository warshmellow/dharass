'''
tweet_processing.py

Contains functions to extract info from JSON tweets and to rehydrate classified
tweets.
'''
from datetime import datetime


def get_text_in_order(tweet_statuses):
    '''
    Returns a list of texts of tweets in the order of tweets,
    where tweets is a list of (hydrated) statuses
    '''
    return [status['text'] for status in tweet_statuses]


def get_text_in_order_from_twitter_api_dump_json(tweets_dump):
    '''
    Returns a list of texts of tweets in the order of tweets,
    where tweets is a json object from Twitter API read into Python
    '''
    return get_text_in_order(tweets_dump['statuses'])


def get_text_in_order_from_twitter_api_dump_json_file(filename):
    '''
    Returns a list of texts of tweets in the order of tweets,
    where tweets is a json file from Twitter API
    '''
    with open(filename) as f:
        tweets_dump = json.load(f)
    return get_text_in_order(tweets_dump['statuses'])


def get_statuses_in_order_from_twitter_api_dump_json_file(filename):
    '''
    Returns a list of (hydrated) statuses of tweets in the order of tweets,
    where tweets is a json file from Twitter API
    '''
    with open(filename) as f:
        tweets_dump = json.load(f)
    return tweets_dump['statuses']


def main():
    pass

if __name__ == '__main__':
    main()
