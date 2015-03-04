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


def apply_and_append_to_twitter_api_dump_json(tweets_dump, key_name, funcs):
    '''
    Applies f in funcs to tweet_dump (following iterator order) 
    then returns a copy of tweet_dump, storing the result as the value
    associated to key_name.
    
    e.g. with tweet_dump, 'labels', [predict], returns copy of tweet_dump with 
    tweet_dump['labels'] = predict(tweet_dump)
    '''
    result = tweets_dump
    for f in funcs:
        result = f(result)
    modified_copy = tweets_dump.copy()
    modified_copy[key_name] = result
    return modified_copy


def predict_and_append_to_twitter_api_dump_json(tweets_dump, label_name, 
    predict_func):
    '''
    Takes a tweets dump and returns a copy with the result of calling
    predict_func (a prediction function like a classifier) stored with the
    key label_name
    '''
    return apply_and_append_to_twitter_api_dump_json(
        tweets_dump, 
        label_name, [
            get_text_in_order_from_twitter_api_dump_json,
            predict_func,
            lambda y: map(lambda x: x[1], y)])


def main():
    pass

if __name__ == '__main__':
    main()
