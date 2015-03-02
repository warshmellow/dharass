'''
tweet_processing.py

Contains functions to extract info from JSON tweets and export to 

Extract username, text of tweet, timestamp from tweet (initially as JSON)
Read in tweet text
return list of username, tweet ids (as given by Twitter), dates
export such list to JSON

Want functions that can pipe into a Pipeline that takes Tweet text content
and returns a classifier.
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
    

def classify_tweets(tweets, vectorizer, classifer):
    "Takes list of Tweets and returns list of all tweets with classification"
    # Expect tweets to be list of full tweet data: the order determines index
    # in classifier
    tweets_as_vectors = vectorizer.transform(
        [status['text'] for status in tweets])
    y_pred = classifer.predict(tweets_as_vectors)
    tweets_with_label = zip(tweets, y_pred)
    return tweets_with_label

def tweets_by_label(tweets_with_label, label=1):
    "Returns all tweets of a certain label (in binary classification, 0 or 1)"
    return [tweet for tweet, label in tweets_with_label if label == label]

def sort_tweets_by_datetime(tweets, reverse=False):
    "Returns tweets sorted by created_at datetime"
    format_str = "%a %b %d %H:%M:%S %z %Y"
    return sorted(tweets, key=lambda tweet: datetime.strptime(
        tweet['created_at'], format_str), reverse=reverse)

def get_user_text_created_at(tweets):
    "Returns user screen name, text, and created_at"
    return [{
        'screen_name': tweet['user']['screen_name'],
        'text': tweet['text'],
        'created_at': tweet['created_at']}
        for tweet in tweets]

def main():
    pass

if __name__ == '__main__':
    main()

