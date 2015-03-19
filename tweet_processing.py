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


def predict_and_append_to_twitter_api_dump_json(tweets_dump,
                                                label_name,
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


def get_info_from_twitter_api_dump_json(tweets_dump):
    'Returns screen name, text, and label if label exists'
    names = [
        status['user']['screen_name']
        for status
        in tweets_dump['statuses']]
    texts = [status['text'] for status in tweets_dump['statuses']]

    if 'label' in tweets_dump:
        return zip(names, texts, tweets_dump['label'])
    else:
        return zip(names, texts)


def apply_to_text_of_twitter_api_query(statuses, funcs):
    '''
    Apply functions in order to statuses texts and get back names,
    texts, results
    '''
    statuses_as_dicts = [status.AsDict() for status in statuses]
    names = [status['user']['screen_name'] for status in statuses_as_dicts]
    texts = [status['text'] for status in statuses_as_dicts]
    results = texts
    for f in funcs:
        results = f(results)
    return zip(names, texts, results)


def main():
    pass

if __name__ == '__main__':
    main()
