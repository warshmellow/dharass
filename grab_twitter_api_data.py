import twitter
import pymongo
from pymongo import MongoClient
import time


def main():
    # Connect to Twitter API
    with open('twitter_app_keys.txt') as f:
        keys = tuple([line.rstrip() for line in list(f)])
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = keys

    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN,
                      access_token_secret=ACCESS_TOKEN_SECRET)
    # Nothing to see by displaying twitter_api except that it's now a
    # defined variable
    print api.VerifyCredentials()

    # Conenct to db
    client = MongoClient('localhost', 27017)
    db = client['dharass']
    collection = db['tweets-dump']

    # Get data every time interval and dump into db
    INTERVAL_SECONDS = 600.0
    start_time = time.time()
    while True:
        print 'Pulling Tweets from Twitter API'
        femfreq_mentions = api.GetSearch(
            term='@femfreq',
            lang='en',
            result_type='recent',
            count=100)

        status_drop_urls = []
        for status in femfreq_mentions:
            result = status.AsDict()
            if 'retweeted_status' in result:
                result['retweeted_status'].pop('urls', None)
            result.pop('urls', None)
            status_drop_urls.append(result)
        
        print "Inserting into MongoDB"
        collection.insert(status_drop_urls)
        
        print "Total Tweets: %d" % collection.count()
        print "Sleeping now"
        time.sleep(
            INTERVAL_SECONDS - ((time.time() - start_time) % INTERVAL_SECONDS))


if __name__ == '__main__':
    main()
