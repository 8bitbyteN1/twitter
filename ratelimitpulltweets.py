import tweepy
import json
from datetime import datetime, timedelta

# enter your API keys and access tokens here
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

# authenticate to Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# enter your search parameters here
keywords = ['your', 'search', 'keywords']
data_dict = ['list', 'of', 'data', 'dictionary', 'words']
start_date = datetime(2022, 1, 1, 0, 0, 0)  # start of time frame
end_date = datetime(2022, 12, 31, 23, 59, 59)  # end of time frame
time_spent = 300  # time to spend downloading tweets in seconds

# initialize list to hold tweets
tweets = []

# initialize time variables
start_time = datetime.now()
elapsed_time = 0

# iterate through all tweets containing the keywords and data dictionary words
for tweet in tweepy.Cursor(api.search_tweets,
                           q=' '.join(keywords + data_dict),
                           tweet_mode='extended',
                           lang='en',
                           since_id=None,
                           count=100,
                           include_entities=True).items():

    # check if tweet is within the time frame
    if start_date <= tweet.created_at <= end_date:
        # add tweet to list
        tweets.append(tweet)

    # check rate limit status
    remaining_time = (datetime.now() - start_time).total_seconds()
    if api.rate_limit_status()['resources']['search']['/search/tweets']['remaining'] == 0 and remaining_time < time_spent:
        # wait for rate limit to reset
        sleep_time = api.rate_limit_status()['resources']['search']['/search/tweets']['reset'] - datetime.now().timestamp()
        print(f'Rate limit reached, waiting {sleep_time} seconds...')
        time.sleep(sleep_time)

    # check if time spent downloading tweets has been reached
    elapsed_time = (datetime.now() - start_time).total_seconds()
    if elapsed_time >= time_spent:
        break

# write tweets to file
with open('tweets.json', 'w') as f:
    json.dump([tweet._json for tweet in tweets], f)
